CARPROOT := /Users/schwifty/Repos/carp-paper/figures
AMRROOT  := /Users/schwifty/Repos/netsketch-amr-profiling/data/figs
ORCAROOT := /Users/schwifty/Repos/mon-paper/tikz-exps/pdf

CARPFILES := 
AMRFILES  := lesson_ordering_v5.pdf msgcnt_regr_vert.pdf
ORCAFILES := sampling.pdf overlay-agg-new.pdf

CARPTARGETS := $(addprefix carp_,$(notdir $(CARPFILES)))
AMRTARGETS  := $(addprefix amr_,$(notdir $(AMRFILES)))
ORCATARGETS := $(addprefix orca_,$(notdir $(ORCAFILES)))

ALLTARGETS := $(CARPTARGETS) $(AMRTARGETS) $(ORCATARGETS)

all: $(ALLTARGETS)

carp_%: 
	cp $(CARPROOT)/$* $@

amr_%: 
	cp $(AMRROOT)/$* $@

orca_%: 
	cp $(ORCAROOT)/$* $@

clean:
	rm -f $(ALLTARGETS)