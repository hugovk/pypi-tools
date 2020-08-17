.PHONY = all clean

SRCS := $(wildcard data/*.json)
PNGS := $(wildcard images/*.png)

.PHONY: all
all: ${PNGS}

images/pip-install-all.png: data/20??-??.json
	python3 jsons2csv.py --chart --no-show --quiet -i "data/20*.json"

images/pip-install-%.png: data/%-????-??.json
	python3 jsons2csv.py --chart --no-show --quiet -i "data/"$*"*.json"
