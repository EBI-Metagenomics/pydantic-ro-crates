# Pydantic-RO-Crates

## Overview

Pydantic-RO-Crates is a Python library for preparing RO-Crates using Pydantic types.
It supports the building of json-ld RO-Crate metadata graphs, as well as preparing rich HTML previews of them.

![Composite screenshots of subset of code from this README example and the rendered html previews](media/pydantic-ro-crate.png "Composite diagram and screenshot")

## Features
- Build crates pythonically, using Pydantic types for all schema.org types
- Include ("localise") certain files _into_ the crate
- Package crates as .zip
- Prepare HTML preview in the crate, as human-readable accompianment to the machine-readable RO-Crate metadata JSON-ld
- Where localised files are previewable (e.g. HTML files from reporting tools), these are linked into a "website in a crate"
- Plugins (`contrib`s) for extra functionality, like making HTML maps

## Installation
```shell
pip install pydantic-ro-crates
```

## Usage

```python
from pydantic2_schemaorg.Dataset import Dataset
from pydantic2_schemaorg.GeoCoordinates import GeoCoordinates

from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import ROOT_PATH, LocalalisableFile

roc = ROCrate()

# define a location metadata - we can use GeoCoordinates type from schema.org
location = GeoCoordinates(
  longitude=14.25,
  latitude=40.808333,
  name="Sample location",
  id_=f"#location-ERS2154049"
)

# add the location entity to the crate:
roc += location

# maybe we need to add a non-standard property to a standard type like the root Dataset
# just inherit the Pydantic type, and add another field!
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

# Use the mapping plugin to make a nice rendered map of the locations
from pydantic_ro_crates.contrib.mapping.render_map import render_leaflet_map
from pathlib import Path
render_leaflet_map([location], output=Path("map.html"), title=dataset.name)

# add the map html file as a "localisable" file; i.e. include it in the packaged crate AND the crate metadata graph
roc.add_localised_file(
   LocalalisableFile(
       id_="map.html",
       source_on_host=Path("map.html"),
       name="Sample map",
       description="Map of sample coordinates"
   )
)

# package the crate as a zip: the metadata json, preview html, and the included map html
roc.zip(Path("my-crate.zip"))
```

> [!NOTE]
> **Citing this work**
> If you find this package useful for academic work and wish to cite it, it is described in a BioHackrXiv preprint:
>
> Rogers A, Bäuerle F, Beracochea M, et al. Enhancing multi-omic analyses through a federated microbiome analysis service. BioHackrXiv; 2025. DOI: 10.37044/osf.io/3x274.

---

## Development

Issues and pull-requests are very welcome.

### Development requirements
`poetry`

### Development installation

1. Clone the repository:
    ```shell
    git clone https://github.com/EBI-Metagenomics/pydantic-ro-crates.git
    cd pydantic-ro-crates
    ```

2. Install with poetry:
    ```shell
    poetry install
    ```

3. Run tests:
   ```shell
   poetry run pytest
   ```
