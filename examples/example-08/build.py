#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from ryland import Ryland
from ryland.tubes import calc_context, path, load, markdown, project


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"


tags = defaultdict(list)


def collect_tags(ryland: Ryland, context: dict) -> dict:
    frontmatter = context["frontmatter"]
    for tag in frontmatter.get("tags", []):
        tags[tag].append(
            ryland.process(
                context,
                project(["frontmatter", "url"]),
            )
        )
    return context


for page_file in sorted(PAGES_DIR.glob("*.md")):
    ryland.render_tubes(
        path(page_file),
        load(),
        markdown(frontmatter=True),
        {"url": f"/{page_file.stem}/"},
        collect_tags,
        {"template_name": "page.html"},
    )


for tag in tags:
    ryland.render_tubes(
        {
            "tag": tag,
            "pages": tags[tag],
            "url": f"/tag/{tag}/",
            "template_name": "tag.html",
        },
    )
