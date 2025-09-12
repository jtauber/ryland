#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from ryland import Ryland
from ryland.tubes import tube, path, load, markdown, project


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"


@tube
def calc_url(_: Ryland, context: dict) -> dict:
    return {
        "url": f"/{context["source_path"].stem}/",
        **context,
    }

tags = defaultdict(list)

@tube
def collect_tags(_: Ryland, context: dict) -> dict:
    frontmatter = context["frontmatter"]
    for tag in frontmatter.get("tags", []):
        tags[tag].append(
            (context | project(["frontmatter", "source_path"]) | calc_url).context(ryland)
        )
    return context


for page_file in sorted(PAGES_DIR.glob("*.md")):
    pipeline = path(page_file) | load | markdown(frontmatter=True) | collect_tags
    ryland.render_pipeline("page.html", f"{page_file.stem}/index.html", pipeline)


for tag, pages in tags.items():
    ryland.render_template("tag.html", f"tag/{tag}/index.html", {
        "tag": tag,
        "pages": pages,
    })
