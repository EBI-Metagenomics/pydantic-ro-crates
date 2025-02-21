from pathlib import Path
from typing import Any, Literal, Optional

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic.v1 import BaseModel, Field

from pydantic_ro_crates.graph.models import LocalalisableFile


class _VegaBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class FormatType(BaseModel):
    type_: Literal["tsv"] = Field(..., alias="type")  # TODO others


class VegaData(_VegaBaseModel):
    url: Optional[str] = Field(None)
    format: Optional[FormatType] = Field(None)
    name: Optional[str] = Field(None)


class VegaEncoding(_VegaBaseModel):
    x: Any  # TODO: use something like https://koxudaxi.github.io/datamodel-code-generator/ to fetch vega schema as pydantic and specify the type here alt.X
    y: Any  # alt.Y
    tooltip: Any


class VegaMark(_VegaBaseModel):
    type: str


class VegaLiteVisualisation(CreativeWork):
    type_: str = Field(default="VegaLiteVisualisation", alias="@type")
    data: VegaData
    mark: VegaMark
    encoding: VegaEncoding
    transform: Any
    title: str
    width: int
    height: int
    encodingFormat: str = Field(default="application/json")


VEGA_LITE_CONTEXT = "vega-lite-context.json"
_VEGA_LITE_CONTEXT_LOCATION = Path(__file__).parent.joinpath(VEGA_LITE_CONTEXT)
assert _VEGA_LITE_CONTEXT_LOCATION.exists()


vega_lite_context_file = LocalalisableFile(
    id_=VEGA_LITE_CONTEXT,
    source_on_host=_VEGA_LITE_CONTEXT_LOCATION,
    name="Vega-Lite JSON-LD Context",
    encodingFormat="application/ld+json",
)
