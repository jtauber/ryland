#!/bin/sh

export COVERAGE_FILE="$(pwd)/.coverage"
coverage erase
(cd example-01 && coverage run -a ./build.py)
(cd example-02 && coverage run -a ./build.py)
(cd example-03 && coverage run -a ./build.py)
(cd example-04 && coverage run -a ./build.py)
(cd example-05 && coverage run -a ./build.py)
(cd example-06 && coverage run -a ./build.py)
(cd example-07 && coverage run -a ./build.py)
(cd example-08 && coverage run -a ./build.py)
(cd example-09 && coverage run -a ./build.py)
