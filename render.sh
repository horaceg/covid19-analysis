#! /bin/bash

"$(which conda | rev | cut -d'/' -f3- | rev)"/bin/python render.py json > dist/static/combined.json