from hashlib import md5
import json
from os import makedirs
from pathlib import Path
from shutil import copy, copytree, rmtree
from typing import Any, Callable, Optional

import jinja2
import markdown as markdown_lib
import yaml


from .tubes import load, markdown, project


class Ryland:
    def __init__(
        self,
        root_file: Optional[str] = None,
        output_dir: Optional[Path] = None,
        template_dir: Optional[Path] = None,
        url_root: Optional[str] = None,
        markdown_extensions: Optional[list[str]] = None,
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

        if markdown_extensions is None:
            markdown_extensions = ["fenced_code", "codehilite", "tables"]

        self.output_dir = output_dir
        self.template_dir = template_dir
        self.url_root = url_root or "/"

        self.global_context = {
            "HASHES": {},
        }

        self._markdown = markdown_lib.Markdown(extensions=markdown_extensions)

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
        self.jinja_env.globals["data"] = load_data
        self.jinja_env.globals["calc_url"] = self.calc_url
        self.jinja_env.globals["url_root"] = self.url_root
        self.jinja_env.filters["markdown"] = self._markdown.convert

    def clear_output(self, exclude: Callable[[Path], bool] = lambda _: False) -> None:
        makedirs(self.output_dir, exist_ok=True)
        for child in self.output_dir.iterdir():
            if exclude(child):
                continue
            else:
                if child.is_dir():
                    rmtree(child)
                else:
                    child.unlink()

    def copy_to_output(
        self, source: Path, dest: Optional[str | Path] = None
    ) -> None:
        target = self.output_dir / (source.name if dest is None else dest)
        makedirs(target.parent, exist_ok=True)
        if source.is_dir():
            copytree(source, target, dirs_exist_ok=True)
        else:
            copy(source, target)

    def write_output(self, output_filename: str, content: str | bytes) -> Path:
        output_path = self.output_dir / output_filename
        makedirs(output_path.parent, exist_ok=True)
        mode = "wb" if isinstance(content, bytes) else "w"
        with open(output_path, mode) as f:
            f.write(content)
        return output_path

    def calc_url(self, arg: dict | str) -> str:
        if isinstance(arg, dict):
            url = arg.get("url", "")
        else:
            url = arg

        if url in self.global_context["HASHES"]:
            url = f"{url}?{self.global_context['HASHES'][url]}"

        return self.url_root + url.lstrip("/")

    def add_hash(self, filename: str) -> None:
        path = self.output_dir / filename
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    key = child.relative_to(self.output_dir).as_posix()
                    self.global_context["HASHES"][key] = make_hash(child)
        else:
            self.global_context["HASHES"][filename] = make_hash(path)

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
                        **self.global_context,
                        **context,
                    }
                )
            )

    def process(self, *tubes) -> dict:
        context = {}
        for tube in tubes:
            if isinstance(tube, dict):
                context = {
                    **context,
                    **{
                        key: value(context) if callable(value) else value
                        for key, value in tube.items()
                    },
                }
            else:
                context = tube(self, context)
        return context

    def render(self, *tubes) -> None:
        context = self.process(*tubes)
        template_name = context["template_name"]
        output_filename = context["url"].lstrip("/")
        if output_filename.endswith("/"):
            output_filename += "index.html"
        self.render_template(template_name, output_filename, context)

    def render_markdown(self, markdown_file: Path, template_name: str) -> None:
        self.render(
            load(markdown_file),
            markdown(frontmatter=True),
            {"url": f"/{markdown_file.stem}/", "template_name": template_name},
        )

    def paginated(
        self, items: list[dict], fields: Optional[list[str]] = None
    ) -> list[dict]:
        def _project(item):
            return project(fields)(self, item) if fields else item

        return [
            self.process(
                items[i],
                {
                    "prev": _project(items[i - 1]) if i > 0 else None,
                    "next": _project(items[i + 1]) if i < len(items) - 1 else None,
                },
            )
            for i in range(len(items))
        ]

    def load_global(self, key: str, filename: str) -> None:
        self.global_context[key] = load_data(filename)

    def set_global(self, key: str, value: Any) -> None:
        self.global_context[key] = value

    def add_filter(self, name: str, func: Callable) -> None:
        self.jinja_env.filters[name] = func

    def add_template_global(self, name: str, value: Any) -> None:
        self.jinja_env.globals[name] = value


def make_hash(path) -> str:
    hasher = md5()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def load_data(filename) -> Any:
    if filename.endswith(".json"):
        return json.load(open(filename))
    elif filename.endswith((".yml", ".yaml")):
        return yaml.safe_load(open(filename))
