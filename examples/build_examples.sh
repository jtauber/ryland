#!/bin/sh

export COVERAGE_FILE="$(pwd)/.coverage"
coverage erase

for dir in example-*; do
    (cd "$dir" && coverage run -a --omit="./build.py" ./build.py)
done

coverage report -m
coverage html
