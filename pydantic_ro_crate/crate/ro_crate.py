import json
import logging
import tempfile
from pathlib import Path
from shutil import copy, make_archive
from typing import Any, List

from ..graph.models import RO_CRATE_METADATA_JSON, LocalalisableFile, ROCrateModel

__all__ = ["ROCrate"]

from ..preview.render import render_preview_html


class ROCrate:
    crate: ROCrateModel
    files: List[LocalalisableFile] = []

    def __init__(self, **kwargs):
        self.crate = ROCrateModel(**kwargs)

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
                json.dump(self.json, crate_json_file)

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
