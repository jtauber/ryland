from hashlib import md5
import json
from os import makedirs
from pathlib import Path
from shutil import copy, copytree, rmtree
from typing import Any, Optional

import jinja2
import markdown


class Ryland:
    def __init__(
        self,
        root_file: Optional[str] = None,
        output_dir: Optional[Path] = None,
        template_dir: Optional[Path] = None,
    ):
        if output_dir is None:
            if root_file is not None:
                output_dir = Path(root_file).parent / "output"
            else:
                raise ValueError("root_file must be provided if output_dir is not")

        if template_dir is None:
            if root_file is not None:
                template_dir = Path(root_file).parent / "templates"
            else:
                raise ValueError("root_file must be provided if template_dir is not")

        self.output_dir = output_dir
        self.template_dir = template_dir

        self.hashes = {}

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
        self.jinja_env.globals["data"] = load_data
        self.jinja_env.filters["markdown"] = markdown_filter

    def clear_output(self) -> None:
        makedirs(self.output_dir, exist_ok=True)
        for child in self.output_dir.iterdir():
            if child.is_dir():
                rmtree(child)
            else:
                child.unlink()

    def copy_to_output(self, source: Path) -> None:
        if source.is_dir():
            dest = self.output_dir / source.name
            copytree(source, dest, dirs_exist_ok=True)
        else:
            copy(source, self.output_dir / source.name)

    def add_hash(self, filename: str) -> None:
        self.hashes[filename] = make_hash(self.output_dir / filename)

    def render_template(
        self, template_name: str, output_filename: str, context: Optional[dict] = None
    ) -> None:
        context = context or {}
        template = self.jinja_env.get_template(template_name)
        output_path = self.output_dir / output_filename
        makedirs(output_path.parent, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(
                template.render(
                    {
                        "HASHES": self.hashes,
                        **context,
                    }
                )
            )


def make_hash(path) -> str:
    hasher = md5()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def markdown_filter(text) -> str:
    return markdown.markdown(text, extensions=["fenced_code", "codehilite", "tables"])


def load_data(filename) -> Any:
    if filename.endswith(".json"):
        return json.load(open(filename))
