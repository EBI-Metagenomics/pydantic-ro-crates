import importlib
import logging
import tempfile
from pathlib import Path
from shutil import copy, make_archive
from typing import Any, List

from pydantic import create_model
from pydantic2_schemaorg import __all__ as AVAILABLE_SCHEMAORG_TYPES
from pydantic2_schemaorg.Thing import Thing

from ..graph.models import (
    CONTEXT,
    GRAPH,
    ID,
    RO_CRATE_CONTEXTS,
    RO_CRATE_METADATA_JSON,
    ROOT_PATH,
    TYPE,
    CrateSubgraphWithAdditionalContexts,
    LocalalisableFile,
    ROCrateMetadata,
    ROCrateModel,
)

__all__ = ["ROCrate"]

from ..preview.render import render_preview_html


class ROCrateParseError(ValueError):
    pass


class ROCrate:
    def __init__(self, files: List[LocalalisableFile] = None, **kwargs):
        self.crate: ROCrateModel = ROCrateModel(**kwargs)
        self.files: List[LocalalisableFile] = files or []

    def add_localised_file(self, localisable_file: LocalalisableFile):
        self.files.append(localisable_file)
        self.graph.append(localisable_file)

    def render(self):
        return self.crate.json(), self.files

    @property
    def graph(self):
        return self.crate.graph_

    @graph.setter
    def graph(self, graph):
        self.crate.graph_ = graph

    @property
    def root(self):
        return self.crate.root

    def __iadd__(self, other: Any):
        if isinstance(other, LocalalisableFile):
            self.add_localised_file(other)
        elif isinstance(other, CrateSubgraphWithAdditionalContexts):
            if type(self.crate.context_) is str:
                self.crate.context_ = [self.crate.context_]
            self.crate.context_ += other.additional_contexts
            for item in other.items:
                self.__iadd__(item)
        else:
            self.crate.graph_.append(other)
        return self

    @property
    def json(self):
        return self.crate.json()

    @property
    def files_suitable_for_preview(self):
        return [file for file in self.files if str(file.id_).endswith(".html")]

    def zip(
        self, filename: Path, force: bool = False, generate_preview: bool = True
    ) -> Path:
        logging.debug(
            f"Should create RO Crate zip as {filename} with {len(self.files)} files"
        )

        if filename.exists() and not force:
            raise FileExistsError

        with tempfile.TemporaryDirectory() as tmpdir:
            logging.info(f"Using {tmpdir} as crate folder")
            with open(tmpdir / Path(RO_CRATE_METADATA_JSON), "w") as crate_json_file:
                logging.debug(f"Dumping crate json to {crate_json_file}")
                crate_json_file.write(self.json)

            if generate_preview:
                render_preview_html(self, tmpdir / Path("ro-crate-preview.html"))

            for file in self.files:
                logging.debug(f"Adding {file.source_on_host} to crate folder")
                if not file.source_on_host.is_file():
                    raise FileNotFoundError(file.source_on_host)
                copy(file.source_on_host, tmpdir / Path(file.id_))

            crate_zip_basename = str(Path(filename.parent) / Path(filename.stem))
            logging.info(f"Zipping crate to {crate_zip_basename}")
            zipfile = make_archive(crate_zip_basename, "zip", tmpdir)
        return Path(zipfile).resolve()

    @classmethod
    def from_json(
        cls, crate_json: dict[str, Any], strict_schemaorg: bool = False
    ) -> "ROCrate":
        incoming_context = crate_json.get(CONTEXT)
        if not incoming_context or not incoming_context in RO_CRATE_CONTEXTS.values():
            raise ROCrateParseError(f"{CONTEXT} of {incoming_context} not supported")

        incoming_graph = crate_json.get(GRAPH)
        if not incoming_graph:
            raise ROCrateParseError(f"{GRAPH} not found in JSON")
        if type(incoming_graph) is not list:
            raise ROCrateParseError(f"{GRAPH} is not a list")
        if len(incoming_graph) < 1:
            raise ROCrateParseError(f"{GRAPH} is empty")

        try:
            root_dataset = next(
                item for item in incoming_graph if item.get(ID) == ROOT_PATH
            )
        except StopIteration:
            raise ROCrateParseError(f"{ROOT_PATH} not found in graph")
        else:
            logging.info(f"Root dataset found {root_dataset}")

        try:
            crate_metadata = next(
                item
                for item in incoming_graph
                if item.get(ID) == RO_CRATE_METADATA_JSON
            )
        except StopIteration:
            raise ROCrateParseError(f"{RO_CRATE_METADATA_JSON} not found in {GRAPH}")
        else:
            logging.info(f"Crate metadata found {crate_metadata}")

        crate_metadata_obj = ROCrateMetadata(**crate_metadata)
        # May fail if crate metadata json contains unexpected keys

        instance = cls()
        instance.crate = ROCrateModel(
            context_=incoming_context, graph_=[crate_metadata_obj]
        )

        for item in incoming_graph:
            logging.info(f"Processing graph item {item.get(ID)}")
            if item.get(ID) == RO_CRATE_METADATA_JSON:
                continue

            incoming_item_type = item.get(TYPE)
            if incoming_item_type is None:
                raise ROCrateParseError(f"{TYPE} not found in {item}")

            logging.debug(
                f"Incoming graph has item of claimed type {incoming_item_type}."
            )
            if incoming_item_type in AVAILABLE_SCHEMAORG_TYPES:
                logging.debug(f"Found {incoming_item_type} in schema.org")
                schemaorg_module = importlib.import_module(
                    f"pydantic2_schemaorg.{incoming_item_type}"
                )
                item_obj = getattr(schemaorg_module, incoming_item_type)(**item)
                instance += item_obj
                logging.info(f"Added {item.get(ID)} to graph")

            elif strict_schemaorg:
                raise ROCrateParseError(
                    f"{incoming_item_type} is not a schema.org type"
                )

            else:
                dynamic_model = create_model(incoming_item_type, __base__=Thing)
                logging.debug(
                    f"Created arbitrary Thing-based model for {incoming_item_type}"
                )
                item_obj = dynamic_model(**item)
                instance += item_obj
                logging.info(f"Added {item.get(ID)} to graph")

        return instance
