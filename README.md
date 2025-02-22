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
from pydantic_ro_crates.graph.models import ROOT_PATH

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
```

### Location `mapping` plugin
**See `examples/sample_map/` for a full example.**
```shell
poetry run python examples/sample_map/make_crate_with_map_of_locations.py
```

This contrib renders maps (using [leaflet.js](https://leafletjs.com/)), for locations specified by `schema.org:GeoCoordinates`.
The rendered map is an HTML file that is attached to the RO-Crate, so that the crate zip file will include it
and the crate preview HTML file will include a link to it.

```python
# <continued from above>

from pydantic_ro_crates.graph.models import LocalalisableFile

# Use the mapping plugin to make a nice rendered map of the locations
from pydantic_ro_crates.contrib.mapping.render_map import render_leaflet_map
from pathlib import Path
render_leaflet_map([location], output=Path("map.html"), title=dataset.name)

# add the map html file as a "localisable" file; i.e. include it in the packaged crate AND the crate metadata graph
roc += LocalalisableFile(
    id_="map.html",
    source_on_host=Path("map.html"),
    name="Sample map",
    description="Map of sample coordinates"
)

# package the crate as a zip: the metadata json, preview html, and the included map html
roc.zip(Path("my-crate.zip"))
```

### Data Visualisation (`dataviz`) plugin
**See `examples/metagenomic_taxonomies/` for a full example.**
```shell
poetry run python examples/metagenomic_taxonomies/make_taxonomy_crate.py
```

> [!WARNING]
> Only one high-level visualisation is provided currently (a weighted histogram of a TSV file).
> Other visualisations can be made using `altair` and the `make_visualisation` method directly.

This contrib helps create and embed [Vega-Lite](https://vega.github.io/vega-lite/) descriptors of *how* a dataset
in the crate could be visualised.
For example, describing the canonical visualisation of a certain TSV file may be a histogram of one of its columns.
It doesn't only *render* the visualisation as an extra preview file in the crate,
it also embeds the Vega Lite specification JSON directly into the crate graph so that consumers of this crate can
use local Vega-compatible libraries to reproduce or modify the suggested visualisation.

```python
from pathlib import Path

from pydantic_ro_crates.crate.ro_crate import ROCrate
from pydantic_ro_crates.graph.models import LocalalisableFile
from pydantic_ro_crates.contrib.dataviz.histogram import tsv_histogram

roc = ROCrate()

# Add the data file itself into the crate, so that it will be packaged alongside the metadata
taxonomy_data = LocalalisableFile(
    source_on_host=Path(__file__).parent / "iss_taxonomies.tsv",
    id_="iss_taxonomies.tsv",
    name="SILVA taxonomic assignments",
    encodingFormat="text/tab-separated-values",
)
roc += taxonomy_data

# Create a histogram of the 20 most prevalent taxa in the TSV file.
# Creates a vega-lite spec (JSON, specified as a new type defined by an additional local context),
# as well as an HTML rendering of this visualisation for crate preview purposes.
viz_subgraph = tsv_histogram(
    data_file=taxonomy_data,
    x_label="taxonomy",
    y_label="SSU_rRNA",
    n_biggest=20,
)

# Add the custom context and the vega-spec JSON to the crate graph, and the rendered HTML file.
roc += viz_subgraph
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
