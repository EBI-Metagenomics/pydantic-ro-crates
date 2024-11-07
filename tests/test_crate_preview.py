import tempfile
from pathlib import Path
from pprint import pprint

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.Dataset import Dataset
from pydantic2_schemaorg.Organization import Organization

from pydantic_ro_crate.crate.ro_crate import ROCrate
from pydantic_ro_crate.preview.render import render_preview_html


def test_crate_preview():
    roc = ROCrate()

    license = CreativeWork(
        id_="https://www.ebi.ac.uk/licencing",
        description="This work is licensed under the EMBL-EBI terms of use",
        identifier="https://www.ebi.ac.uk/licencing",
        name="Licensing of EMBL-EBI data resources",
    )
    roc += license

    org = Organization(
        id_="https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00006683"
    )
    roc += org

    study = Dataset(
        id_="./",
        name="Temporal diversity and community structure of the planktonic protist assemblage",
        description="Detailed sequencing study of protist diversity at the LTER station MareChiara, Gulf of Naples, using V4 Illumina sequencing.",
        datePublished="2024-08-01T08:26:41",
        publisher=org.id_,
        license=license.id_,
    )
    roc += study

    pprint(roc.json)

    with tempfile.TemporaryDirectory() as tmpdir:
        html = render_preview_html(roc, tmpdir / Path("preview.html"))

        assert "This work is licensed under the EMBL-EBI terms of use" in html
        assert "<script>" in html

        assert (tmpdir / Path("preview.html")).is_file()
