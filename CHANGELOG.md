# Changelog

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
