#!/usr/bin/env bash

python3 jsons2img.py --chart -i "data/20*.json"
python3 jsons2img.py --chart -p attrs
python3 jsons2img.py --chart -p black
python3 jsons2img.py --chart -p certifi
python3 jsons2img.py --chart -p cibuildwheel
python3 jsons2img.py --chart -p colorama
python3 jsons2img.py --chart -p coverage
python3 jsons2img.py --chart -p cryptography
python3 jsons2img.py --chart -p cython
python3 jsons2img.py --chart -p django
python3 jsons2img.py --chart -p flake8
python3 jsons2img.py --chart -p flask
python3 jsons2img.py --chart -p html5lib
python3 jsons2img.py --chart -p httpx
python3 jsons2img.py --chart -p humanize
python3 jsons2img.py --chart -p matplotlib
python3 jsons2img.py --chart -p nose2
python3 jsons2img.py --chart -p numpy
python3 jsons2img.py --chart -p pandas
python3 jsons2img.py --chart -p paramiko
python3 jsons2img.py --chart -p pillow
python3 jsons2img.py --chart -p pip
python3 jsons2img.py --chart -p prettytable
python3 jsons2img.py --chart -p pycodestyle
python3 jsons2img.py --chart -p pyflakes
python3 jsons2img.py --chart -p pylast
python3 jsons2img.py --chart -p pylint
python3 jsons2img.py --chart -p pytest
python3 jsons2img.py --chart -p pytest-cov
python3 jsons2img.py --chart -p python-dateutil
python3 jsons2img.py --chart -p pytz
python3 jsons2img.py --chart -p requests
python3 jsons2img.py --chart -p rich
python3 jsons2img.py --chart -p ruff
python3 jsons2img.py --chart -p scikit-learn
python3 jsons2img.py --chart -p scipy
python3 jsons2img.py --chart -p setuptools
python3 jsons2img.py --chart -p six
python3 jsons2img.py --chart -p sphinx-lint
python3 jsons2img.py --chart -p tablib
python3 jsons2img.py --chart -p tensorflow
python3 jsons2img.py --chart -p termcolor
python3 jsons2img.py --chart -p tox
python3 jsons2img.py --chart -p tqdm
python3 jsons2img.py --chart -p twitter
python3 jsons2img.py --chart -p ujson
python3 jsons2img.py --chart -p urllib3
python3 jsons2img.py --chart -p uv
python3 jsons2img.py --chart -p virtualenv
python3 jsons2img.py --chart -p wheel

open images/*.png
