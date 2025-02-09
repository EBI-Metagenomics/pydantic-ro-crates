from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader
from pydantic2_schemaorg.GeoCoordinates import GeoCoordinates

template_dir = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(template_dir))


def render_leaflet_map(
    coordinates: List[GeoCoordinates], output: Optional[Path] = None, title: str = "Map"
) -> str:
    template = env.get_template("leaflet.j2")

    html_output = template.render(
        title=title, coordinates=[(c.latitude, c.longitude) for c in coordinates]
    )

    if output:
        with output.open("w") as f:
            f.write(html_output)

    return html_output
