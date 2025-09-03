# Ryland

A simple static site generation library


## Current Features

- Jinja2 templates and a basic markdown filter
- copying static files and directory trees (for stylesheets, scripts, fonts, images)
- cache-busting with hashes


## History

I've generally found most static site generation libraries to either be far too complex for my needs or be too restricted to just blogs so, over the years, I've generated many static sites with lightweight, bespoke Python code and hosted them on GitHub pages. However, I've ended up repeating myself a lot so I'm now cleaning it all up and generalizing my prior work as this library.


## Example Usage

For now, clone this repo and use as an editable requirement.

Write a build script of the following form:

```python
from ryland import Ryland

ROOT_DIR = Path(__file__).parent.parent
DIST_DIR = ROOT_DIR / "dist"
PANTRY_DIR = ROOT_DIR / "pantry"
TEMPLATE_DIR = ROOT_DIR / "templates"

ryland = Ryland(dist_dir=DIST_DIR, template_dir=TEMPLATE_DIR)

ryland.clear_dist()
ryland.copy_to_dist(PANTRY_DIR / "style.css")
ryland.calc_hash("style.css")

ryland.render_template("404.html", "404.html")
ryland.render_template("about_us.html", "about-us/index.html")

# construct context variables

ryland.render_template("homepage.html", "index.html", {
    # context variables
})
```

## Cache-Busting Hashes

The `calc_hash` makes it possible to do

```html
<link rel="stylesheet" href="/style.css?{{ HASHES['style.css'] }}">
```

in the templates.


## Markdown Filter

To render a markdown context variable:

```
{{ content | markdown }}
```

## Sites Currently Using Ryland

- <https://projectamaze.com>


## Roadmap

- move over other sites to use Ryland
- incorporate more common elements that emerge
- produce a Ryland-generated website for Ryland
- document how to automatically build with GitHub actions
- write up a cookbook
- add a command-line too for starting a Ryland-based site

