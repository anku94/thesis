CARPROOT := /Users/schwifty/Repos/carp-paper/figures
AMRROOT  := /Users/schwifty/Repos/netsketch-amr-profiling/data/figs
ORCAFIGSROOT := /Users/schwifty/Repos/mon-paper/data/figs
ORCATIKZROOT := /Users/schwifty/Repos/mon-paper/data/tikz-figs-new

CARPFILES := distrib6.pdf distrib.amr.pdf distrib.vpic.pdf
CARPEVALFILES := qlatvssel.v6.pdf runtime.v4.werr.pdf query.ycsb.v3.pdf pvtbench.adapt.pdf rtp.latvspvtcnt.pdf pvtbench.epxpp.pdf carpdb.impact.alt4.pdf load.vs.params.pdf runtime.vs.params.pdf
AMRFILES  := msgcnt_regr.pdf msgcnt_regr_hor.pdf lesson_volfunc_v2_short_zoom.pdf lesson_throttling_v4.pdf lesson_ordering_v5.pdf criticalpath2.pdf criticalpath.pdf sendorder_v2.pdf octree.pdf blastwave_runtime.pdf blastwave_runtime_wide.pdf blastwave_tradeoff_wide_mini.pdf blastwave_comm_wide_mini.pdf meshdriver_locbench.pdf scaling.pdf
ORCAFIGSFILES := lesson_volfunc_zoom.pdf lesson_volfunc_single.pdf lesson_volfunc_single_cdf.pdf amr_tracer_runtimes.pdf amr_tracer_runtimes_2x2.pdf amr_tracesizes_line.pdf query_suite.pdf query_suite_abs.pdf dftracer_comp.pdf ofi_tcp_tracer_runtimes.pdf ontv_combined.pdf agentic_timeline.pdf
ORCATIKZFILES := arch.pdf plan.pdf plan2.pdf ts2pc.pdf

CARPTARGETS := $(addprefix carp_,$(CARPFILES)) $(addprefix carp_,$(CARPEVALFILES))
AMRTARGETS  := $(addprefix amr_,$(AMRFILES))
ORCATARGETS := $(addprefix orca_,$(ORCAFIGSFILES)) $(addprefix orca_,$(ORCATIKZFILES))

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

# ORCA figures from data/figs
orca_lesson_volfunc_zoom.pdf: $(ORCAFIGSROOT)/lesson_volfunc_zoom.pdf
	cp $< $@
orca_amr_tracer_runtimes.pdf: $(ORCAFIGSROOT)/amr_tracer_runtimes.pdf
	cp $< $@
orca_amr_tracer_runtimes_2x2.pdf: $(ORCAFIGSROOT)/amr_tracer_runtimes_2x2.pdf
	cp $< $@
orca_amr_tracesizes_line.pdf: $(ORCAFIGSROOT)/amr_tracesizes_line.pdf
	cp $< $@
orca_query_suite.pdf: $(ORCAFIGSROOT)/query_suite.pdf
	cp $< $@
orca_query_suite_abs.pdf: $(ORCAFIGSROOT)/query_suite_abs.pdf
	cp $< $@
orca_dftracer_comp.pdf: $(ORCAFIGSROOT)/dftracer_comp.pdf
	cp $< $@
orca_ofi_tcp_tracer_runtimes.pdf: $(ORCAFIGSROOT)/ofi_tcp_tracer_runtimes.pdf
	cp $< $@
orca_ontv_combined.pdf: $(ORCAFIGSROOT)/ontv_combined.pdf
	cp $< $@
orca_agentic_timeline.pdf: $(ORCAFIGSROOT)/agentic_timeline.pdf
	cp $< $@
orca_lesson_volfunc_single.pdf: $(ORCAFIGSROOT)/lesson_volfunc_single.pdf
	cp $< $@
orca_lesson_volfunc_single_cdf.pdf: $(ORCAFIGSROOT)/lesson_volfunc_single_cdf.pdf
	cp $< $@

# ORCA figures from tikz-figs-new
orca_arch.pdf: $(ORCATIKZROOT)/arch.pdf
	cp $< $@
orca_plan.pdf: $(ORCATIKZROOT)/plan.pdf
	cp $< $@
orca_plan2.pdf: $(ORCATIKZROOT)/plan2.pdf
	cp $< $@
orca_ts2pc.pdf: $(ORCATIKZROOT)/ts2pc.pdf
	cp $< $@

clean:
	rm -f $(ALLTARGETS)
