#!/usr/bin/env python

from ryland import Ryland


ryland = Ryland(__file__)
ryland.clear_output()
ryland.render_template("homepage.html", "index.html")
