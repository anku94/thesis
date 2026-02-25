# TikZ figures Makefile
# Builds all standalone .tex files to pdf/

# Exclude non-standalone files
EXCLUDE := motifs.tex assets.tex carp-common.tex nordcolors.tex
SOURCES := $(filter-out $(EXCLUDE),$(wildcard *.tex))
PDFS := $(patsubst %.tex,pdf/%.pdf,$(SOURCES))

.PHONY: all clean tidy

all: tidy pdf $(PDFS)

pdf:
	mkdir -p pdf

pdf/%.pdf: %.tex motifs.tex
	latexmk -pdf -synctex=0 -output-directory=pdf -auxdir=build $<

# Remove top-level PDFs and synctex (one-time cleanup)
tidy:
	rm -f *.pdf *.synctex.gz

# Clean build artifacts
clean:
	rm -rf build/*
	rm -rf pdf/*
