from hashlib import md5
from os import makedirs
from shutil import copy, copytree, rmtree

import jinja2
import markdown


class Ryland:
    def __init__(self, dist_dir, template_dir):
        self.dist_dir = dist_dir
        self.template_dir = template_dir
        self.hashes = {}

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
        self.jinja_env.filters["markdown"] = markdown_filter

    def clear_dist(self):
        for child in self.dist_dir.iterdir():
            if child.is_dir():
                rmtree(child)
            else:
                child.unlink()

    def copy_to_dist(self, source):
        if source.is_dir():
            dest = self.dist_dir / source.name
            copytree(source, dest, dirs_exist_ok=True)
        else:
            copy(source, self.dist_dir / source.name)

    def calc_hash(self, filename):
        self.hashes[filename] = make_hash(self.dist_dir / filename)

    def render_template(self, template_name, output_filename, context=None):
        context = context or {}
        template = self.jinja_env.get_template(template_name)
        output_path = self.dist_dir / output_filename
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


def make_hash(path):
    hasher = md5()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def markdown_filter(text):
    return markdown.markdown(text, extensions=["fenced_code", "codehilite", "tables"])
