CARPROOT := /Users/schwifty/Repos/carp-paper/figures
AMRROOT  := /Users/schwifty/Repos/netsketch-amr-profiling/data/figs
ORCAROOT := /Users/schwifty/Repos/mon-paper/tikz-exps/pdf

CARPFILES := distrib6.pdf distrib.amr.pdf distrib.vpic.pdf
AMRFILES  := lesson_ordering_v5.pdf msgcnt_regr_vert.pdf
ORCAFILES := sampling.pdf overlay-agg-new.pdf

CARPTARGETS := $(addprefix carp_,$(notdir $(CARPFILES)))
AMRTARGETS  := $(addprefix amr_,$(notdir $(AMRFILES)))
ORCATARGETS := $(addprefix orca_,$(notdir $(ORCAFILES)))

ALLTARGETS := $(CARPTARGETS) $(AMRTARGETS) $(ORCATARGETS)

all: $(ALLTARGETS)

carp_%: $(CARPROOT)/%
	cp $< $@

amr_%: $(AMRROOT)/%
	cp $< $@

orca_%: $(ORCAROOT)/%
	cp $< $@

clean:
	rm -f $(ALLTARGETS)