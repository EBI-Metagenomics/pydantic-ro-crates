from pathlib import Path

from pydantic_ro_crates.contrib.dataviz.histogram import tsv_histogram
from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import LocalalisableFile


def test_data_visualisation():
    roc = ROCrate()

    datafile = LocalalisableFile(
        source_on_host=Path("tests/fixtures/iss_taxonomies.tsv"),
        id_="iss_taxonomies.tsv",
        name="Taxonomic annotations of a sample from the International Space Station",
    )

    roc += datafile

    taxonomy_data = LocalalisableFile(
        source_on_host=Path(__file__).parent / "fixtures" / "iss_taxonomies.tsv",
        id_="iss_taxonomies.tsv",
        name="SILVA taxonomic assignments",
        encodingFormat="text/tab-separated-values",
    )
    roc += taxonomy_data

    viz_subgraph = tsv_histogram(
        data_file=taxonomy_data,
        x_label="taxonomy",
        y_label="SSU_rRNA",  # OTU counts
        n_biggest=20,
    )

    roc += viz_subgraph

    assert "vega-lite-context.json" in viz_subgraph.additional_contexts
    assert "vega-lite-context.json" in roc.crate.context_
    assert len(viz_subgraph.items) == 3  # html, json context, vega spec
