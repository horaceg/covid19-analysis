#! /bin/bash

conda install -c conda-forge --file requirements.txt
"$(which conda | rev | cut -d'/' -f3- | rev)"/bin/pip install PyMuPDF