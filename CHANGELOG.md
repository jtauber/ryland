# Changelog

## 0.14.0

- removed `markdown-full-yaml-metadata` in favour of doing it ourselves (to avoid conflicts with built-in extensions like wikilinks)

## 0.13.0

- `load` tube now sets `source_modified` with the last modified date of the file
- `Ryland.load_global` can be used to load a context from a file that will be included in all templates

## 0.12.0

- Ryland can be configured with a `url_root` for generation at something other than `/`
- added `calc_url` function that uses `url_root`, automatically adds the cache-busting hash, and optionally takes an context with a `url` value
- added new example (which also changes the way tags are done to take advantage of `calc_url`)

## 0.11.0

- added `excerpt` tube factory to extract the first paragraph of a page
- added `paginated` method that decorates a list of page contexts with next/prev
- added an example illustrating both

## 0.10.0

- implemented new "tubes" approach where context transformations can be chained together
- added `process` method to execute tubes
- added `render` method to process tubes to get a context for template rendering and output
- initial tubes in `ryland.tubes`: `project`, `load`, `markdown`, `debug`
- added helped function `get_context` for retrieving from context with dotted path notation and defaults
- added two more examples using all the above to support tagging and frontmatter-overriding of template and url

## 0.9.0

- `render_markdown` now supports YAML frontmatter
- added example

## 0.8.0

- added `render_markdown` method
- added example
- upgraded to `markdown>=3.9`

## 0.7.0

- `data` function now supports YAML
- added two examples of the `data` function

## 0.6.0

- removed `strftime` filter (can just use `.strftime` instead)

## 0.5.0

- added `strftime` filter
- include `markdown-full-yaml-metadata`
- added a third example

## 0.4.0

- `clear_output` will create the directory if it doesn't exist
- added another example

## 0.3.0

- changed `dist` to `output`
- changed `calc_hash` to `add_hash`
- support just passing in `__file__` and assuming `output_dir` and `template_dir`
- added an example

## 0.2.0

- added the `data` function with support for JSON

## 0.1.0

- initial release
