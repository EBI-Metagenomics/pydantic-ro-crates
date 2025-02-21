from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Union

from pydantic import BaseModel
from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.Dataset import Dataset
from pydantic2_schemaorg.MediaObject import MediaObject
from pydantic2_schemaorg.SchemaOrgBase import SchemaOrgBase
from pydantic.v1 import Field, validator

__all__ = [
    "Dataset",
    "GRAPH",
    "CONTEXT",
    "TYPE",
    "ID",
    "ROCrateModel",
    "File",
    "LocalalisableFile",
    "RO_CRATE_METADATA_JSON",
    "ROCrateMetadata",
    "CrateSubgraphWithAdditionalContexts",
]

from pydantic2_schemaorg.Thing import Thing

GRAPH = "@graph"
CONTEXT = "@context"
TYPE = "@type"
ID = "@id"
ABOUT = "about"
CONFORMS_TO = "conformsTo"
ROOT_PATH = "./"


class RO_CRATE_VERSIONS(str, Enum):
    ONE_ZERO = "1.0"
    ONE_ONE = "1.1"
    LATEST = ONE_ONE


RO_CRATE_CONTEXTS = {
    RO_CRATE_VERSIONS.ONE_ZERO: "https://w3id.org/ro/crate/1.0/context",
    RO_CRATE_VERSIONS.ONE_ONE: "https://w3id.org/ro/crate/1.1/context",
}

RO_CRATE_PROFILE_BASE = "https://w3id.org/ro/crate/"

RO_CRATE_PROFILES = {
    RO_CRATE_VERSIONS.ONE_ZERO: RO_CRATE_PROFILE_BASE + RO_CRATE_VERSIONS.ONE_ZERO,
    RO_CRATE_VERSIONS.ONE_ONE: RO_CRATE_PROFILE_BASE + RO_CRATE_VERSIONS.ONE_ONE,
}

RO_CRATE_METADATA_JSON = "ro-crate-metadata.json"


class ROCrateMetadata(CreativeWork):
    id_: Any = Field(default=RO_CRATE_METADATA_JSON, alias="@id", frozen=True)
    conforms_to_: Any = Field(
        default=RO_CRATE_PROFILES[RO_CRATE_VERSIONS.LATEST], alias=CONFORMS_TO
    )
    about: Optional[Union[List[Union["Thing", str]], "Thing", str]] = Field(
        default=ROOT_PATH, alias=ABOUT
    )


class ROCrateModel(SchemaOrgBase):
    context_: Optional[Any] = Field(
        default=RO_CRATE_CONTEXTS[RO_CRATE_VERSIONS.LATEST], alias="@context"
    )

    @staticmethod
    def maybe_get_crate_metadata_entity(graph: List[Any]) -> Optional[ROCrateMetadata]:
        if not graph:
            return None
        for entity in graph:
            if type(entity) is ROCrateMetadata:
                return entity

    @validator("graph_", pre=True, always=True)
    def ensure_metadata_is_in_graph(cls, graph: List[Any]) -> List[Any]:
        if graph and cls.maybe_get_crate_metadata_entity(graph):
            return graph
        elif graph:
            return [ROCrateMetadata()] + graph
        else:
            return [ROCrateMetadata()]

    @property
    def root(self):
        # https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html#finding-the-root-data-entity
        if not self.graph_:
            raise ValueError("Graph does not exist")
        root = None
        for entity in self.graph_:
            if entity.conforms_to_ and str(entity.conforms_to_).startswith(
                RO_CRATE_PROFILE_BASE
            ):
                root = entity.about
                break
        if root:
            for entity in self.graph_:
                if entity.id_ == root:
                    return entity
            raise ValueError("No root entity found")
        else:
            raise ValueError("No root descriptor found")


class File(MediaObject):
    type_: str = Field(default="File", alias="@type", const=True)


class LocalalisableFile(File):
    source_on_host: Path = Field(exclude=True)


class CrateSubgraphWithAdditionalContexts(BaseModel):
    additional_contexts: List[Union[str, dict]]
    items: List[Any]
