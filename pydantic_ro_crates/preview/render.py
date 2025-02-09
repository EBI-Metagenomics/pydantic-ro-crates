from pathlib import Path
from typing import TYPE_CHECKING, Optional

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from pydantic_ro_crates.crate.ro_crate import ROCrate

template_dir = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(template_dir))


def render_preview_html(roc: "ROCrate", output: Optional[Path] = None) -> str:
    template = env.get_template("crate-preview.j2")

    html_output = template.render(
        name=roc.root.name,
        description=roc.root.description,
        entities=roc.graph,
        local_files=roc.files,
        pages=roc.files_suitable_for_preview,
    )

    if output:
        with output.open("w") as f:
            f.write(html_output)

    return html_output
