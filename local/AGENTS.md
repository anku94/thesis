Our goal here is to bootstrap a Latex PhD thesis from paper text.

There are four sources to incorporate:

- The thesis proposal as the base for the full thesis, copied verbatim from /Users/schwifty/Repos/thesis/proposal/
- CARP: /Users/schwifty/Repos/carp-paper
- AMR: /Users/schwifty/Repos/netsketch-amr-profiling
- ORCA: /Users/schwifty/Repos/mon-paper

Note that CARP was written in my 3rd year, AMR in my 6th year, and ORCA in my 7th year, so I have evolved conventions by ORCA time that need to be backported into CARP/AMR.

At no point should you modify anything in any other repo beyond this one.

I need a hierarchical structure for the tex in the thesis:

main.tex
tex/01-carp/01-intro.tex
tex/02-amr/01-intro.tex
tex/03-orca/01-intro.tex
tex/99-figs.tex

For figures:
data/figs/carp-xyz.pdf # renamed
data/figs/carp-x.pdf # renamed

For bib:
bib/carp.bib
bbi/amr.bib

# Basic Instructions
1. CARP and AMR are "settled" papers, while ORCA is being actively refined. I don't know what the takeaway is, but I'd be more hesitant about renaming etc with ORCA because things may update.
2. CARP-time, I managed the bib manually, AMR onwards the bib is auto-exported from Zotero. It is okay to copy the snapshotted bib in the repos, but some keys might be renamed etc, just be careful of that.
3. All figures should be macros in 99-figs.tex -- like \figCarpEvalRuntime. I liek concise hierarchical names. Same for labels. fig:carp:eval-runtime. Or if there's subfigures they should be fig:carp:eval-runtime-word
4. We want to include things using \include not \input.
5. At any point if some instruction doesn't make sense or if there's a conflict say so.
6. For now we're not worried too much about the intra-thesis layout. Just incorporate all content and make it compile. Proposal first then CARP etc.
7. Adopt a "cautious autonomy" style. I am very particular about things. Progress needs to be committed by me frequently. Take baby steps, ask me to check/commit, acquire autonomy only as confidence builds.
8. Do use the latexindent.yaml and .latexmkrc from ORCA
9. For any tex you copy, strip comments.
10. As you discover other rules/conventions while working, add them to the following section.

# LLM-Learned Rules

1. This is a monorepo: `thesis/proposal/` is the proposal, `thesis/thesis/` is the full thesis. Work in `thesis/thesis/`.
