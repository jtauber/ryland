#!/usr/bin/env python

from pathlib import Path
from ryland import Ryland


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

posts = [
    {
        "title": "First Post",
        "content": "This is the **first** post.",
    },
    {
        "title": "Second Post",
        "content": "This is the **second** post.",
    },
    {
        "title": "Third Post",
        "content": "This is the **third** post.",
    },
]

ryland.render_template(
    "homepage.html",
    "index.html",
    {
        "posts": posts,
    },
)
