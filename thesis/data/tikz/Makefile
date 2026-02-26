# TikZ figures Makefile
# Builds all standalone .tex files to pdf/

# Exclude non-standalone files
EXCLUDE := motifs.tex assets.tex
SOURCES := $(filter-out $(EXCLUDE),$(wildcard *.tex))
PDFS := $(patsubst %.tex,pdf/%.pdf,$(SOURCES))
ASSETS := assets.tex $(wildcard assets/*.tex)

# SVG targets (explicit list)
SVG_SOURCES := bsp.tex application.tex
SVGS := $(patsubst %.tex,svg/%.svg,$(SVG_SOURCES))

.PHONY: all clean tidy svg svg-dir

all: tidy pdf $(PDFS)

pdf:
	mkdir -p pdf

pdf/%.pdf: %.tex $(ASSETS)
	latexmk -pdf $<
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

# Clean build artifacts
clean:
	rm -rf build/*
	rm -rf pdf/*
	rm -rf svg/*
