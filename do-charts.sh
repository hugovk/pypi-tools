#!/usr/bin/env bash

python3 jsons2csv.py --chart --no-show -i "data/201*.json"
python3 jsons2csv.py --chart --no-show -i "data/coverage*.json"
python3 jsons2csv.py --chart --no-show -i "data/flake8*.json"
python3 jsons2csv.py --chart --no-show -i "data/django*.json"
python3 jsons2csv.py --chart --no-show -i "data/matplotlib*.json"
python3 jsons2csv.py --chart --no-show -i "data/numpy*.json"
python3 jsons2csv.py --chart --no-show -i "data/pillow*.json"
python3 jsons2csv.py --chart --no-show -i "data/pip*.json"
python3 jsons2csv.py --chart --no-show -i "data/pylast*.json"
python3 jsons2csv.py --chart --no-show -i "data/pylint*.json"
python3 jsons2csv.py --chart --no-show -i "data/pytest*.json"
python3 jsons2csv.py --chart --no-show -i "data/six*.json"
python3 jsons2csv.py --chart --no-show -i "data/tensorflow*.json"
python3 jsons2csv.py --chart --no-show -i "data/pandas*.json"
open data/pip-install-*.png
