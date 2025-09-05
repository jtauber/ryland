# Ryland

A simple static site generation library


## Current Features

- Jinja2 templates with a basic markdown filter and a function to pull data directly from JSON files
- copying static files and directory trees (for stylesheets, scripts, fonts, images)
- cache-busting with hashes


## History

I've generally found most static site generation libraries to either be far too complex for my needs or be too restricted to just blogs so, over the years, I've generated many static sites with lightweight, bespoke Python code and hosted them on GitHub pages. However, I've ended up repeating myself a lot so I'm now cleaning it all up and generalizing my prior work as this library.


## Changelog

### 0.1.0

- initial release

### 0.2.0

- added the `data` function with support for JSON

### 0.3.0

- changed `dist` to `output`
- changed `calc_hash` to `add_hash`
- support just passing in `__file__` and assuming `output_dir` and `template_dir`
- added an example

### 0.4.0

- `clear_output` will create the directory if it doesn't exist
- added another example

### 0.5.0

- added `strftime` filter
- include `markdown-full-yaml-metadata`
- added a third example


## Example Usage

`pip install ryland` (or equivalent).

The write a build script of the following form:

```python
from ryland import Ryland

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
PANTRY_DIR = ROOT_DIR / "pantry"
TEMPLATE_DIR = ROOT_DIR / "templates"

ryland = Ryland(output_dir=OUTPUT_DIR, template_dir=TEMPLATE_DIR)

ryland.clear_output()
ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

ryland.render_template("404.html", "404.html")
ryland.render_template("about_us.html", "about-us/index.html")

# construct context variables

ryland.render_template("homepage.html", "index.html", {
    # context variables
})
```

Also see `examples/` in this repo.


## Cache-Busting Hashes

The `add_hash` makes it possible to do

```html
<link rel="stylesheet" href="/style.css?{{ HASHES['style.css'] }}">
```

in the templates to bust the browser cache when a change is made to a stylesheet, script, etc.


## Markdown Filter

To render a markdown context variable:

```html
{{ content | markdown }}
```


## Data Function

To pull data directly from a JSON file in a template:

```html
<div>
  <h2>Latest News</h2>

  {% for news_item in data("news_list.json")[:3] %}
    <div>
      <div class="news-dateline">{{ news_item.dateline }}</div>
      <p>{{ news_item.content }}</p>
    </div>
  {% endfor %}
</div>
```

## Sites Currently Using Ryland

- <https://projectamaze.com>
- <https://digitaltolkien.com>


## Roadmap

In no particular order:

- move over other sites to use Ryland
- incorporate more common elements that emerge
- add support for YAML data loading in templates
- improve error handling
- produce a Ryland-generated website for Ryland
- document how to automatically build with GitHub actions
- write up a cookbook
- add a command-line tool for starting a Ryland-based site
