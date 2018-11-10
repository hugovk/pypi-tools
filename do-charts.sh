#!/usr/bin/env bash
python3 jsons2csv.py --chart --no-show -i "data/201*"
python3 jsons2csv.py --chart --no-show -i "data/django*"
python3 jsons2csv.py --chart --no-show -i "data/matplotlib*"
python3 jsons2csv.py --chart --no-show -i "data/numpy*"
python3 jsons2csv.py --chart --no-show -i "data/pillow*"
python3 jsons2csv.py --chart --no-show -i "data/pylast*"
open data/pip-install-*.png
