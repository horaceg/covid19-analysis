#!/bin/bash

set -x

./download.sh

mkdir -p data
$CONDA_PREFIX/bin/python parsing.py
$CONDA_PREFIX/bin/python parsing.py us

$CONDA_PREFIX/bin/python combine.py
$CONDA_PREFIX/bin/python combine.py us
