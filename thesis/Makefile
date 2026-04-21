DRAFT_DIR := data/drafts
DRAFT_NAME := $(shell date '+%Y%m%d_%H00')

.PHONY: all clean

all:
	latexmk main.tex
	@mkdir -p $(DRAFT_DIR)
	cp build/main.pdf $(DRAFT_DIR)/$(DRAFT_NAME).pdf
	@echo "Saved $(DRAFT_DIR)/$(DRAFT_NAME).pdf"

clean:
	latexmk -C main.tex
