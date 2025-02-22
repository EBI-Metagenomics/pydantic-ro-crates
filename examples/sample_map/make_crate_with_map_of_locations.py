from pydantic2_schemaorg.Dataset import Dataset
from pydantic2_schemaorg.GeoCoordinates import GeoCoordinates

from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import ROOT_PATH, LocalalisableFile

# initialize an RO-Crate
roc = ROCrate()

# define a location metadata - we can use GeoCoordinates type from schema.org
location = GeoCoordinates(
    longitude=14.25,
    latitude=40.808333,
    name="Sample location",
    id_=f"#location-ERS2154049",
)

# add the location entity to the crate:
roc += location


# maybe we need to add a non-standard property to a standard type like the root Dataset
# just inherit the Pydantic type, and add another field!
# This field should really be defined in a new Type definition/context,
# but pragmatically sometimes crates do include extra non-standard properties on a type.
class DataSetWithLocation(Dataset):
    location: GeoCoordinates


# now make the root dataset - this is core to the RO-Crate spec
dataset = DataSetWithLocation(
    id_=ROOT_PATH,
    name="Sample ERS2154049 - Mediterranean surface marine water",
    description="Mediterranean surface marine water, part of study of protist temporal diversity",
    identifier="ERS2154049",
    location=location,
)
# add root dataset to the crate, too
roc += dataset

from pathlib import Path

# Use the mapping plugin to make a nice rendered map of the locations
from pydantic_ro_crates.contrib.mapping.render_map import render_leaflet_map

render_leaflet_map([location], output=Path("map.html"), title=dataset.name)

# add the map html file as a "localisable" file; i.e. include it in the packaged crate AND the crate metadata graph
roc += LocalalisableFile(
    id_="map.html",
    source_on_host=Path("map.html"),
    name="Sample map",
    description="Map of sample coordinates",
)

# package the crate as a zip: the metadata json, preview html, and the included map html
roc.zip(Path("marine_sample.zip"), force=True)
