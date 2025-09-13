#!/usr/bin/env python

from pathlib import Path
from ryland import Ryland
from ryland.tubes import load, markdown

ROOT_DIR = Path(__file__).parent
PANTRY_DIR = ROOT_DIR / "pantry"
PAGES_DIR = ROOT_DIR / "pages"

ryland = Ryland(__file__)
ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

ryland.load_global("site", "site.yaml")

context = ryland.process(load(PAGES_DIR / "home.md"), markdown())
ryland.render_template("page.html", "index.html", context)
