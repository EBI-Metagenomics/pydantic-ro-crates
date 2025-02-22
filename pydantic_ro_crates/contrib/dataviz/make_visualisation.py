import logging
import tempfile
from pathlib import Path
from typing import Optional

import altair as alt
import pandas as pd

from pydantic_ro_crates.contrib.dataviz.VegaLiteVisualisation import (
    VEGA_LITE_CONTEXT,
    FormatType,
    VegaData,
    VegaLiteVisualisation,
    vega_lite_context_file,
)
from pydantic_ro_crates.graph.models import (
    CrateSubgraphWithAdditionalContexts,
    LocalalisableFile,
)


def make_visualisation(
    data_file: LocalalisableFile,
    chart_definition: alt.Chart,
    url_format: Optional[FormatType] = None,
    html_output_on_host: Optional[Path] = None,
) -> CrateSubgraphWithAdditionalContexts:

    if not url_format:
        url_format = FormatType(type="tsv")

    chart = chart_definition

    df = None
    if url_format.type_ == "tsv":
        df = pd.read_csv(data_file.source_on_host, sep="\t")
    else:
        logging.warning(
            "Cannot determine type of data file for loading visualisation data as dataframe"
        )

    data_name = Path(data_file.id_).stem

    if df is not None:
        logging.debug(
            f"Read dataframe {data_file.source_on_host} with columns: {df.columns}, and {len(df)} rows"
        )
        html_name = data_name + "_viz.html"
        html_output_dir = html_output_on_host or Path(tempfile.gettempdir())
        chart.properties(data=df).save(html_output_dir / html_name)

        html_localisable_file = LocalalisableFile(
            id_=html_name,
            source_on_host=(html_output_dir / html_name),
            name=f"Visualisation of {data_file.id_}",
        )
    else:
        html_localisable_file = None

    vega_spec = VegaLiteVisualisation.parse_obj(chart.properties().to_dict())
    vega_spec.id_ = f"{data_file.id_}-vega-lite-spec"
    vega_spec.name = f"Visualisation of {data_file.id_}"

    vega_spec.data = VegaData(
        url=data_file.id_,
        format=url_format,
    )

    return CrateSubgraphWithAdditionalContexts(
        additional_contexts=[VEGA_LITE_CONTEXT],
        items=(
            [vega_lite_context_file, vega_spec] + [html_localisable_file]
            if html_localisable_file
            else []
        ),
    )
