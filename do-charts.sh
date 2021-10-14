#!/usr/bin/env bash

python3 jsons2csv.py --chart --no-show -i "data/20*.json"
python3 jsons2csv.py --chart --no-show -p attrs
python3 jsons2csv.py --chart --no-show -p black
python3 jsons2csv.py --chart --no-show -p colorama
python3 jsons2csv.py --chart --no-show -p coverage
python3 jsons2csv.py --chart --no-show -p cryptography
python3 jsons2csv.py --chart --no-show -p django
python3 jsons2csv.py --chart --no-show -p flake8
python3 jsons2csv.py --chart --no-show -p html5lib
python3 jsons2csv.py --chart --no-show -p httpx
python3 jsons2csv.py --chart --no-show -p humanize
python3 jsons2csv.py --chart --no-show -p matplotlib
python3 jsons2csv.py --chart --no-show -p nose2
python3 jsons2csv.py --chart --no-show -p numpy
python3 jsons2csv.py --chart --no-show -p pandas
python3 jsons2csv.py --chart --no-show -p paramiko
python3 jsons2csv.py --chart --no-show -p pillow
python3 jsons2csv.py --chart --no-show -p pip
python3 jsons2csv.py --chart --no-show -p prettytable
python3 jsons2csv.py --chart --no-show -p pycodestyle
python3 jsons2csv.py --chart --no-show -p pyflakes
python3 jsons2csv.py --chart --no-show -p pylast
python3 jsons2csv.py --chart --no-show -p pylint
python3 jsons2csv.py --chart --no-show -p pytest
python3 jsons2csv.py --chart --no-show -p pytest-cov
python3 jsons2csv.py --chart --no-show -p python-dateutil
python3 jsons2csv.py --chart --no-show -p pytz
python3 jsons2csv.py --chart --no-show -p requests
python3 jsons2csv.py --chart --no-show -p scikit-learn
python3 jsons2csv.py --chart --no-show -p scipy
python3 jsons2csv.py --chart --no-show -p setuptools
python3 jsons2csv.py --chart --no-show -p six
python3 jsons2csv.py --chart --no-show -p tablib
python3 jsons2csv.py --chart --no-show -p tensorflow
python3 jsons2csv.py --chart --no-show -p tox
python3 jsons2csv.py --chart --no-show -p tqdm
python3 jsons2csv.py --chart --no-show -p twitter
python3 jsons2csv.py --chart --no-show -p ujson
python3 jsons2csv.py --chart --no-show -p urllib3
python3 jsons2csv.py --chart --no-show -p virtualenv
python3 jsons2csv.py --chart --no-show -p wheel

open images/*.png
