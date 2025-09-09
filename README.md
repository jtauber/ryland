# Ryland

A simple static site generation library


## Current Features

- use of Jinja2 templates
- render page-level markdown
- render markdown within data using filter
- pull data directly from JSON or YAML files within templates
- copy static files and directory trees (for stylesheets, scripts, fonts, images)
- generate hash for cache-busting


## History

I've generally found the framework-approach of most static site generators to either be far too complex for my needs or too restricted to just blogs or similar. Over the years, I've generated many static sites with lightweight, bespoke Python code and hosted them on GitHub pages. I've ended up repeating myself a lot so I'm now cleaning it all up and generalizing my prior work as this library.


## Changelog

Now see `CHANGELOG.md`


## Example Usage

`pip install ryland` (or equivalent).

Then write a build script of the following form:

```python
from ryland import Ryland

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
PANTRY_DIR = ROOT_DIR / "pantry"
TEMPLATE_DIR = ROOT_DIR / "templates"

ryland = Ryland(output_dir=OUTPUT_DIR, template_dir=TEMPLATE_DIR)

ryland.clear_output()

## copy and hash static files

ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

## render templates

ryland.render_template("404.html", "404.html")
ryland.render_template("about_us.html", "about-us/index.html")

# construct context variables

ryland.render_template("homepage.html", "index.html", {
    # context variables
})

## and/or generate from Markdown files

PAGES_DIR = Path(__file__).parent / "pages"

for page_file in PAGES_DIR.glob("*.md"):
    ryland.render_markdown(page_file, "page.html")
```

Also see `examples/` in this repo.


## Cache-Busting Hashes

The `add_hash` makes it possible to do

```html
<link rel="stylesheet" href="/style.css?{{ HASHES['style.css'] }}">
```

in the templates to bust the browser cache when a change is made to a stylesheet, script, etc.


## `markdown` Filter

To render a markdown context variable:

```html
{{ content | markdown }}
```


## Data Function

You can put together your template context in your Python build script or you can pull data directly from a JSON or YAML file within a template.

Here's an example of the latter:

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
- <https://jktauber.com>


## Roadmap

In no particular order:

- move over other sites to use Ryland
- incorporate more common elements that emerge
- improve error handling
- produce a Ryland-generated website for Ryland
- document how to automatically build with GitHub actions
- write up a cookbook
- add a command-line tool for starting a Ryland-based site

Because Ryland is a library, a lot of missing features can just be implemented by the site developer.
However, if three or more sites duplicate effort in their build script, I'll consider at least adding helper code to Ryland.

Once five independent people are running sites built with Ryland, I will declare 1.0.0.
