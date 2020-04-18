#!/bin/bash

set -x

./download.sh

$CONDA_PREFIX/bin/python parsing.py
$CONDA_PREFIX/bin/python parsing.py us

$CONDA_PREFIX/bin/python combine.py
$CONDA_PREFIX/bin/python combine.py us
