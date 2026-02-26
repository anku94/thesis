WIP prompt for ppts

Do read AGENTS.md first

## Staged Buildouts

0. If I say `reload` that means reload this prompt
1. `StagedBuildout` class is in `common.py` (not staged_buildout.py which is legacy)
2. Outputs go to `data/figs/sb/` via `save_plot(fig, fname, subdir="sb")`

## Workflow for creating sb_ files

1. Create `sb_<xyz>.py` for plot `<xyz>.py`
2. Import data/helpers from original (reuse what's reusable)
3. Duplicate plotting code with outer/inner structure intact (allows independent control of aspect ratios, fonts for presentations)
4. Keep original function names (plot_runtime_line, not plot_sb)
5. Add separate `sb_<name>(fig, ax)` function for frame generation, called from outer function (comment out to skip frames)

## StagedBuildout API

- `StagedBuildout(ax, fig, fname, ext="pdf")`
- `add_frame(artists, legend_items, xtick_items)`
- `build()` - saves `data/figs/sb/{fname}_{idx}.{ext}`
- Legend management only works with ax.legend (skipped for fig.legend)

## Notes

- Use `ppt.mplstyle` (not `paper.mplstyle`) for presentations - larger fonts, line widths, marker sizes
- Always inspect artist indices empirically before defining frames (don't guess)
- Debug: `for i, a in enumerate(ax.get_children()): print(i, type(a).__name__, getattr(a, 'get_label', lambda: '')())`
