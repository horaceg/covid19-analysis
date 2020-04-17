#! /bin/bash

"$(which conda | rev | cut -d'/' -f2- | rev)"/python render.py json > dist/static/combined.json