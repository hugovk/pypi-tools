.PHONY = all clean

SRCS := $(wildcard data/*.json)
PNGS := $(wildcard images/*.png)

.PHONY: all
all: ${PNGS}

images/all.png: data/20??-??.json
	python3 jsons2img.py --chart --quiet -i "data/20*.json"

images/%.png: data/%-????-??.json
	python3 jsons2img.py --chart --quiet -p $*

## data       to fetch new data
.PHONY: data
data:
	./get-data.sh

## compress   to compress images
.PHONY: compress
compress:
	time ls images/*.png | parallel --bar optipng -o7 -zm1-9 {}

## monthly    to do a monthly update
.PHONY: monthly
monthly:
	$(MAKE) data
	$(MAKE) -j 10
	$(MAKE) compress
	pre-commit run --all-files

.PHONY: help
help : Makefile
	@echo "Please use \`make <target>' where <target> is one of"
	@sed -n 's/^##//p' $<
