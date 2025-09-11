#!/usr/bin/env python

from pathlib import Path
from ryland import Ryland


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"

for page_file in PAGES_DIR.glob("*.md"):
    ryland.render_markdown(page_file, "page.html")
