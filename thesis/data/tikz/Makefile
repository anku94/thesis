# TikZ figures Makefile
# Builds all standalone .tex files to pdf/

# Exclude non-standalone files
EXCLUDE := motifs.tex assets.tex
SOURCES := $(filter-out $(EXCLUDE),$(wildcard *.tex))
PDFS := $(patsubst %.tex,pdf/%.pdf,$(SOURCES))
ASSETS := assets.tex $(wildcard assets/*.tex)

# SVG targets (explicit list)
SVG_SOURCES := bsp.tex application.tex orca-arch.tex floop-orca.tex carp-layout.tex svg-test.tex
SVGS := $(patsubst %.tex,svg/%.svg,$(SVG_SOURCES))

SVGALT_SOURCES := application.tex carp-layout.tex
SVGALTS := $(patsubst %.tex,svgalt/%.svg,$(SVGALT_SOURCES))

.PHONY: all clean tidy svg svg-dir svgalt svgalt-dir

all: tidy pdf $(PDFS)

pdf:
	mkdir -p pdf

pdf/%.pdf: %.tex $(ASSETS)
	latexmk $<
	cp build/$*.pdf $@

# Remove top-level PDFs and synctex (one-time cleanup)
tidy:
	rm -f *.pdf *.synctex.gz

# SVG conversion
svg: $(SVGS)

svg/%.svg: pdf/%.pdf | svg-dir
	pdftocairo -svg $< $@

svg-dir:
	mkdir -p svg

# Alternate SVG conversion using DVI to preserve SVG text nodes
svgalt: $(SVGALTS)

svgalt/%.svg: %.tex $(ASSETS) | svgalt-dir
	latex -interaction=nonstopmode -halt-on-error -output-directory=build $<
	dvisvgm build/$*.dvi -o build/$*.svg
	python3 transform-svg.py build/$*.svg $@

svgalt-dir:
	mkdir -p svgalt

# Clean build artifacts
clean:
	rm -rf build/*
	rm -rf pdf/*
	rm -rf svg/*
	rm -rf svgalt/*
