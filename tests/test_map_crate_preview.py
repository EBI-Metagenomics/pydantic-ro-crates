import tempfile
from pathlib import Path

from pydantic2_schemaorg.Dataset import Dataset
from pydantic2_schemaorg.GeoCoordinates import GeoCoordinates

from pydantic_ro_crates.contrib.mapping.render_map import render_leaflet_map
from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import ROOT_PATH, LocalalisableFile


def test_map_crate_preview():
    roc = ROCrate()

    location = GeoCoordinates(
        longitude=14.25,
        latitude=40.808333,
        name="Sample location",
        id_=f"#location-ERS2154049",
    )
    roc += location

    class DataSetWithLocation(Dataset):
        location: GeoCoordinates

    dataset = DataSetWithLocation(
        id_=ROOT_PATH,
        name="Sample ERS2154049 - Mediterranean surface marine water",
        description="Mediterranean surface marine water, part of study of protist temporal diversity",
        identifier="ERS2154049",
        location=location,
    )
    roc += dataset

    with tempfile.TemporaryDirectory() as leaflet_dir:
        leaflet_file = leaflet_dir / Path("map.html")
        render_leaflet_map([location], leaflet_file, title=dataset.name)

        roc.add_localised_file(
            LocalalisableFile(
                id_="map.html",
                source_on_host=leaflet_file,
                name="Sample map",
                description="Map of sample coordinates",
            )
        )

        roc.zip(Path("map-test.zip"), force=True)
