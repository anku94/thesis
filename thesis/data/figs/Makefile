CARPROOT := /Users/schwifty/Repos/carp-paper/figures
AMRROOT  := /Users/schwifty/Repos/netsketch-amr-profiling/data/figs
ORCAROOT := /Users/schwifty/Repos/mon-paper/data/tikz-exps/pdf

CARPFILES := distrib6.pdf distrib.amr.pdf distrib.vpic.pdf
CARPEVALFILES := qlatvssel.v6.pdf runtime.v4.werr.pdf query.ycsb.v3.pdf pvtbench.adapt.pdf rtp.latvspvtcnt.pdf pvtbench.epxpp.pdf carpdb.impact.alt4.pdf load.vs.params.pdf runtime.vs.params.pdf
AMRFILES  := lesson_ordering_v5.pdf msgcnt_regr_vert.pdf blastwave_runtime_wide.pdf lesson_volfunc_v2_short_zoom.pdf
ORCAFILES := sampling.pdf overlay-agg-new.pdf

CARPTARGETS := $(addprefix carp_,$(CARPFILES)) $(addprefix carp_,$(CARPEVALFILES))
AMRTARGETS  := $(addprefix amr_,$(AMRFILES))
ORCATARGETS := $(addprefix orca_,$(ORCAFILES))

CARPDESIGNTARGETS := carp_layout_v2.pdf carp_arch_v12mini.pdf carp_sender_wobg_v6.pdf carp_reneg_hists_v4.pdf carp_carpdb_log_v3.pdf

ALLTARGETS := $(CARPTARGETS) $(AMRTARGETS) $(ORCATARGETS) $(CARPDESIGNTARGETS)

all: $(ALLTARGETS)

carp_distrib%: $(CARPROOT)/distrib%
	cp $< $@

carp_%: $(CARPROOT)/eval/%
	cp $< $@

carp_layout_v2.pdf: $(CARPROOT)/design/carp_layout_v2.pdf
	cp $< $@

carp_arch_v12mini.pdf: $(CARPROOT)/design/carp_arch_v12mini.pdf
	cp $< $@

carp_sender_wobg_v6.pdf: $(CARPROOT)/design/carp_sender_wobg_v6.pdf
	cp $< $@

carp_reneg_hists_v4.pdf: $(CARPROOT)/design/reneg_hists_v4.pdf
	cp $< $@

carp_carpdb_log_v3.pdf: $(CARPROOT)/design/carpdb_log_v3.pdf
	cp $< $@

amr_%: $(AMRROOT)/%
	cp $< $@

orca_%: $(ORCAROOT)/%
	cp $< $@

clean:
	rm -f $(ALLTARGETS)
