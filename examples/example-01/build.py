#!/usr/bin/env python

from pathlib import Path

from ryland import Ryland

ROOT_DIR = Path(__file__).parent
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATE_DIR = ROOT_DIR / "templates"

ryland = Ryland(dist_dir=OUTPUT_DIR, template_dir=TEMPLATE_DIR)

ryland.clear_dist()

ryland.render_template("homepage.html", "index.html")
