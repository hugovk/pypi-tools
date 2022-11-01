.PHONY = all clean

SRCS := $(wildcard data/*.json)
PNGS := $(wildcard images/*.png)

.PHONY: all
all: ${PNGS}

images/all.png: data/20??-??.json
	python3 jsons2csv.py --chart --no-show --quiet -i "data/20*.json"

images/%.png: data/%-????-??.json
	python3 jsons2csv.py --chart --no-show --quiet -p $*

## data       to fetch new data
.PHONY: data
data:
	./get-data.sh

## compress   to compress images
.PHONY: compress
compress:
	time ls images/*.png | parallel optipng -o7 -zm1-9 {}

.PHONY: help
help : Makefile
	@echo "Please use \`make <target>' where <target> is one of"
	@sed -n 's/^##//p' $<
