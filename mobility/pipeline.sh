#!/bin/bash

set -x

./download.sh

python parsing.py
python parsing.py us

python combine.py
python combine.py us
