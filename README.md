# Ryland

A simple static site generation library


## Current Features

- use of Jinja2 templates
- render page-level markdown including frontmatter support
- render markdown within data using filter
- pull data directly from JSON or YAML files within templates
- copy static files and directory trees (for stylesheets, scripts, fonts, images)
- generate hash for cache-busting
- built-in and custom compositional context transformations ("tubes") including ability to calculate some context variables from others


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

or, for more control, context transformations (or "tubes") can be explicitly composed together:

```python
for page_file in sorted(PAGES_DIR.glob("*.md")):
    ryland.render(
        load(page_file),
        markdown(frontmatter=True),
        excerpt(),
        {"url": f"/{page_file.stem}/"},
        collect_tags(),
        {"template_name": "page.html"},
    )
```

Also see `examples/` in this repo.


## Alternative Initialization

If your output directory is `./output/` and your template directory is `./templates/` (relative to the build script), you can just initialize with:

```python
ryland = Ryland(__file__)
```

`Ryland` also takes a `url_root` if the generated site will live somewhere other than directly under `/`.

The `calc_url` function (below) can be helpful in constructing urls that honour this.


## Cache-Busting Hashes

The `add_hash` makes it possible to do

```html
<link rel="stylesheet" href="/style.css?{{ HASHES['style.css'] }}">
```

in the templates to bust the browser cache when a change is made to a stylesheet, script, etc.

Note that `calc_url` (see below) will automatically add the hash if one exists, so the following is equivalent:

```html
<link rel="stylesheet" href="{{ calc_url('style.css') }}">
```


## Render Markdown Method

`ryland.render_markdown` takes a `Path` to a Markdown file and a template name.

The Markdown is rendered to HTML and passed to the template as `content`. The YAML frontmatter (if it exists) is passed to the template as `frontmatter`.

Under the covers, this is just a `render` call with a pre-defined set of tubes (see below) but is handy for just rendering a Markdown file to HTML with Jinja2 templating.


## Paginated Method

`ryland.paginated` takes a list of contexts and added a `next` and `prev` to each of them.

For example:

```python
>>> ryland.paginated([{"post": "foo"}, {"post": "bar"}])
[{'post': 'foo', 'prev': None, 'next': {'post': 'bar'}}, {'post': 'bar', 'prev': {'post': 'foo'}, 'next': None}]
```

or, to give a real-world example:

```python
posts = [
    ryland.process(
        load(post_file),
        markdown(frontmatter=True),
        {"url": f"/{post_file.stem}/"},
        {"template_name": "post.html"},
    )
    for post_file in sorted(POSTS_DIR.glob("*.md"))
]
for post in ryland.paginated(posts, fields=["url", "frontmatter"]):
    ryland.render(post)
```

`ryland.paginated` takes an optional `fields` parameter to project which context variables are included in `next` and `prev`.


## Markdown Filter

To render a markdown context variable:

```html
{{ content | markdown }}
```


## Calc URL Function

The template function `calc_url` will honour the `url_root` and will automatically add the cache-busting hash if one exists.

So if the `url_root` is `/my-site/` and `style.css` has been hashed, then `{{ calc_url('style.css') }}` will be expanded to `/my-site/style.css?HASH`.

If `calc_url` is given a context (dictionary) rather than a string, the `url` value will be used. This enables things like

`<a href="{{ calc_url(page) }}">` if, for example, `page` is the context for the page being linked to.


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


## Tubes

A "tube" is a function that takes a context dictionary and returns a new one while also being able to access the Ryland instance.

Built-in tube factories in `ryland.tubes` include the follow:

- `load(source_path: Path)` loads the given path and puts it on the context as `source_path`, the last modified datetime as `source_modified`, and the contents as `source_content`.
- `markdown(frontmatter=False)` converts the Markdown in `source_content` to HTML and puts it in `content`. Optionally puts the YAML frontmatter in `frontmatter`.
- `excerpt()` extracts the first paragraph of `content` and puts it in `excerpt`.
- `debug(pretty=True)` outputs the context at that point to stderr (by default pretty-printing it).
- `project(keys: list[str])` keeps only the listed keys in the context.

Developers can write their own tubes or tube factories, for example here to collect pages by tag:

```python
tags = defaultdict(list)

def collect_tags():
    def tube(ryland: Ryland, context: Dict[str, Any]) -> Dict[str, Any]:
        frontmatter = context["frontmatter"]
        for tag in frontmatter.get("tags", []):
            tags[tag].append(
                ryland.process(
                    context,
                    project(["frontmatter", "url", "excerpt"]),
                )
            )
        return context
    return tube
```

This builds up a dictionary `tags` which, for each tag, contains a list of contexts containing the frontmatter, url, and excerpt for each page with that tag in its frontmatter.

## Process Method 

The `ryland.process` method takes a series of dictionaries and tubes and builds up a new context.

## Render Method

The `ryland.render` method processes a series of dictionary and tubes and then uses the resultant context to render a template. The template name is given by `template_name` in the context and the output path is determined by the `url` in the context.

For example:

```python
for tag in tags:
    ryland.render(
        {
            "tag": tag,
            "pages": tags[tag],
            "url": f"/tag/{tag}/",
            "template_name": "tag.html",
        },
    )
```

## The Get Context Helper

`ryland.helpers.get_context` allows the retrieval of values from a context using dotted path notation and with defaulting.

For example, in 

```python
for page_file in sorted(PAGES_DIR.glob("*.md")):
    ryland.render(
        load(page_file),
        markdown(frontmatter=True),
        excerpt(),
        {"url": get_context("frontmatter.url", f"/{page_file.stem}/")},
        collect_tags(),
        {"template_name": get_context("frontmatter.template_name", "page.html")},
    )
```

the `url` and `template_name` can be overridden in the page's frontmatter.


## Load Global Method

If you have a file that contains information that should be available in every template (such as site information) you can load it with `load_global`:

```python
ryland.load_global("site", "site_info.yaml")
```

## Sites Currently Using Ryland

- <https://projectamaze.com>
- <https://digitaltolkien.com>
- <https://jktauber.com>
- <https://cite.digitaltolkien.com>


## Other Projects Building on Ryland

- <https://github.com/jtauber/ryland-blog-template>


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
