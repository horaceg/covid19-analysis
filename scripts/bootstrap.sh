#! /bin/bash

conda install -c conda-forge --file requirements.txt
sudo apt-get install gcc libpq-dev -y
sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y
pip3 install wheel
pip install PyMuPDF