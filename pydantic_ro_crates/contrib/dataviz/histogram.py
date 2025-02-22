import logging
from collections.abc import Callable

import altair as alt

from pydantic_ro_crates.contrib.dataviz.make_visualisation import make_visualisation
from pydantic_ro_crates.contrib.dataviz.VegaLiteVisualisation import FormatType
from pydantic_ro_crates.graph.models import (
    CrateSubgraphWithAdditionalContexts,
    LocalalisableFile,
)


def tsv_histogram(
    data_file: LocalalisableFile,
    x_label: str,
    y_label: str = "count",
    title_factory: Callable[[LocalalisableFile], str] = lambda f: f.name,
    n_biggest: int = None,
    **kwargs,
) -> CrateSubgraphWithAdditionalContexts:
    histogram_definition = (
        alt.Chart()
        .mark_bar()
        .encode(
            x=alt.X(f"{x_label}:N", title=x_label, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y(f"{y_label}:Q", title=y_label, axis=alt.Axis(labelAngle=-45)),
            tooltip=[
                alt.Tooltip(f"{x_label}:N", title=x_label),
                alt.Tooltip(f"{y_label}:Q", title=y_label),
            ],
        )
        .properties(
            title=title_factory(data_file),
            width=kwargs.get("width", 800),
            height=kwargs.get("height", 400),
        )
    )
    if n_biggest is not None:
        logging.debug(f"Filtering to the top at most {n_biggest} rows by {y_label}")
        histogram_definition = histogram_definition.transform_window(
            rank=f"rank({y_label})", sort=[alt.SortField(y_label, order="descending")]
        ).transform_filter(alt.datum.rank <= n_biggest)

    return make_visualisation(
        data_file=data_file,
        chart_definition=histogram_definition,
        url_format=FormatType(type="tsv"),
        **kwargs,
    )
