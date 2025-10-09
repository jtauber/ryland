#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, TypeAlias
from ryland import Ryland
from ryland.helpers import get_context
from ryland.tubes import load, markdown, project


Context: TypeAlias = Dict[str, Any]


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"


tags = defaultdict(list)


def collect_tags():
    def inner(ryland: Ryland, context: Context) -> Context:
        for tag in get_context("frontmatter.tags", [])(context):
            tags[tag].append(
                ryland.process(
                    context,
                    project(["frontmatter", "url"]),
                )
            )
        return context

    return inner


for page_file in sorted(PAGES_DIR.glob("*.md")):
    ryland.render(
        load(page_file),
        markdown(frontmatter=True),
        {"url": get_context("frontmatter.url", f"/{page_file.stem}/")},
        collect_tags(),
        {"template_name": get_context("frontmatter.template_name", "page.html")},
    )


for tag in tags:
    ryland.render(
        {
            "tag": tag,
            "pages": tags[tag],
            "url": f"/tag/{tag}/",
            "template_name": "tag.html",
        },
    )
