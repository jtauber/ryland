# Example 02

This example builds on Example 01 and demonstrates both copying of static files and cache-busting them with a hash.

By convention, I use `pantry` for the location of static files that need to be added to the mix when building a site.

```sh
# in a virtual env with Ryland installed

./build.py
(cd output; python -m http.server)

# visit localhost:8000 in a browser
```
