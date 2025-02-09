from pydantic_ro_crates.crate.ro_crate import ROCrate


def test_parse_from_json():
    valid_crate = {
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

    crate = ROCrate.from_json(valid_crate)
    assert crate is not None
    assert len(crate.graph) == 3
