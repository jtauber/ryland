#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from ryland import Ryland
from ryland.tubes import tube, calc_context, path, load, markdown, project


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"


calc_url = calc_context(
    {
        "url": lambda context: f"/{context['source_path'].stem}/",
    }
)


tags = defaultdict(list)


@tube
def collect_tags(_: Ryland, context: dict) -> dict:
    frontmatter = context["frontmatter"]
    for tag in frontmatter.get("tags", []):
        tags[tag].append(
            (context | project(["frontmatter", "source_path"]) | calc_url).context(
                ryland
            )
        )
    return context


for page_file in sorted(PAGES_DIR.glob("*.md")):
    ryland.render_pipeline(
        "page.html",
        f"{page_file.stem}/index.html",
        (path(page_file) | load | markdown(frontmatter=True) | collect_tags),
    )


for tag, pages in tags.items():
    ryland.render_pipeline(
        "tag.html",
        f"tag/{tag}/index.html",
        (
            {"tag": tag, "pages": pages}
            | calc_context({"url": lambda context: f"/tag/{context['tag']}/"})
        ),
    )
