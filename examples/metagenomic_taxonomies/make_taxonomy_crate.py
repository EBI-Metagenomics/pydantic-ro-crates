from pathlib import Path

from pydantic2_schemaorg.Dataset import Dataset

from pydantic_ro_crates.contrib.dataviz.histogram import tsv_histogram
from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import ROOT_PATH, LocalalisableFile

roc = ROCrate()

dataset = Dataset(
    id_=ROOT_PATH,
    name="Taxonomies of metagenomic sample SRS541458",
    description="SILVA taxonomic annotations for metagenomic sample SRS541458 taken from International Space Station",
)
roc += dataset

# Add the data file into the crate, so that it will be packaged alongside the metadata
mapseq_data = LocalalisableFile(
    source_on_host=Path(__file__).parent / "iss_taxonomies.tsv",
    id_="iss_taxonomies.tsv",
    name="SILVA taxonomic assignments",
    encodingFormat="text/tab-separated-values",
)
roc.add_localised_file(mapseq_data)

viz_subgraph = tsv_histogram(
    data_file=mapseq_data,
    x_label="taxonomy",
    y_label="SSU_rRNA",  # OTU counts
    n_biggest=20,
)

roc += viz_subgraph

roc.zip(Path("iss_taxonomies.zip"), force=True)

# run this like: poetry run python examples/metagenomic_taxonomies/make_taxonomy_crate.py
