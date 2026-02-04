CARPROOT := /Users/schwifty/Repos/carp-paper/figures
AMRROOT  := /Users/schwifty/Repos/netsketch-amr-profiling/data/figs
ORCAROOT := /Users/schwifty/Repos/mon-paper/data/tikz-exps/pdf

CARPFILES := distrib6.pdf distrib.amr.pdf distrib.vpic.pdf
CARPEVALFILES := qlatvssel.v6.pdf runtime.v4.werr.pdf
AMRFILES  := lesson_ordering_v5.pdf msgcnt_regr_vert.pdf blastwave_runtime_wide.pdf lesson_volfunc_v2_short_zoom.pdf
ORCAFILES := sampling.pdf overlay-agg-new.pdf

CARPTARGETS := $(addprefix carp_,$(CARPFILES)) $(addprefix carp_,$(CARPEVALFILES))
AMRTARGETS  := $(addprefix amr_,$(AMRFILES))
ORCATARGETS := $(addprefix orca_,$(ORCAFILES))

ALLTARGETS := $(CARPTARGETS) $(AMRTARGETS) $(ORCATARGETS) carp_arch_v12mini.pdf

all: $(ALLTARGETS)

carp_distrib%: $(CARPROOT)/distrib%
	cp $< $@

carp_%: $(CARPROOT)/eval/%
	cp $< $@

carp_arch_v12mini.pdf: $(CARPROOT)/design/carp_arch_v12mini.pdf
	cp $< $@

amr_%: $(AMRROOT)/%
	cp $< $@

orca_%: $(ORCAROOT)/%
	cp $< $@

clean:
	rm -f $(ALLTARGETS)
