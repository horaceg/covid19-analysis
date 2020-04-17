#! /bin/bash

conda install -c conda-forge --file requirements.txt
"$(which conda | rev | cut -d'/' -f2- | rev)"/pip install PyMuPDF