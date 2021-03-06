.PHONY = all clean

SRCS := $(wildcard data/*.json)
PNGS := $(wildcard images/*.png)

.PHONY: all
all: ${PNGS}

images/all.png: data/20??-??.json
	python3 jsons2csv.py --chart --no-show --quiet -i "data/20*.json"

images/%.png: data/%-????-??.json
	python3 jsons2csv.py --chart --no-show --quiet -p $*
