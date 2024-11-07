# { "@context": "https://w3id.org/ro/crate/1.1/context",
#   "@graph": [
#     {
#       "@type": "CreativeWork",
#       "@id": "ro-crate-metadata.json",
#       "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
#       "about": {"@id": "./"}
#     },
#     {
#       "@id": "./",
#       "@type": [
#         "Dataset"
#       ],
#       "hasPart": [
#         {
#           "@id": "cp7glop.ai"
#         },
#         {
#           "@id": "lots_of_little_files/"
#         }
#       ]
#     },
#     {
#       "@id": "cp7glop.ai",
#       "@type": "File",
#       "name": "Diagram showing trend to increase",
#       "contentSize": "383766",
#       "description": "Illustrator file for Glop Pot",
#       "encodingFormat": "application/pdf"
#     },
#     {
#       "@id": "lots_of_little_files/",
#       "@type": "Dataset",
#       "name": "Too many files",
#       "description": "This directory contains many small files, that we're not going to describe in detail."
#     }
#   ]
# }
import tempfile
import zipfile
from pathlib import Path

from pydantic2_schemaorg.CreativeWork import CreativeWork

from pydantic_ro_crate.crate.ro_crate import ROCrate
from pydantic_ro_crate.graph.models import GRAPH, ID, LocalalisableFile


def test_minimal_crate_construction():
    expected = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@type": "CreativeWork",
                "@id": "ro-crate-metadata.json",
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                "about": {"@id": "./"},
            },
            {
                "@id": "./",
                "identifier": "https://doi.org/10.4225/59/59672c09f4a4b",
                "@type": "Dataset",
                "datePublished": "2017",
                "name": "Data files associated with the manuscript:Effects of facilitated family case conferencing for ...",
                "description": "Palliative care planning for nursing home residents with advanced dementia ...",
                "license": {
                    "@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/"
                },
            },
            {
                "@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
                "@type": "CreativeWork",
                "description": "This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Australia License.",
                "identifier": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
                "name": "Attribution-NonCommercial-ShareAlike 3.0 Australia (CC BY-NC-SA 3.0 AU)",
            },
        ],
    }

    roc = ROCrate()
    assert roc.crate.graph_[0].id_ == expected[GRAPH][0][ID]

    license = CreativeWork(
        id_="https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
        description="This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Australia License.",
        identifier="https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
        name="Attribution-NonCommercial-ShareAlike 3.0 Australia (CC BY-NC-SA 3.0 AU)",
    )
    roc.graph.append(license)
    assert len(roc.graph) == 2
    assert roc.graph[1].name == expected[GRAPH][2]["name"]

    roc.add_localised_file(
        LocalalisableFile(
            source_on_host=Path("tests/fixtures/hello_world.txt"),
            id_="hello_world.txt",
            name="Message to the planet",
        )
    )
    assert len(roc.graph) == 3
    assert roc.graph[2].name == "Message to the planet"

    # print(roc.crate.json(indent=2))

    with tempfile.TemporaryDirectory() as tmpdir:
        roc_zip = roc.zip(tmpdir / Path("test-archive"))

        assert roc_zip.is_file()
        zip = zipfile.ZipFile(roc_zip)
        files = zip.namelist()
        assert "ro-crate-metadata.json" in files
        assert "hello_world.txt" in files
