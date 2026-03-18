from runtime import *

from common import StagedBuildout


class TotalData(TypedDict):
    nranks: int
    totals: np.ndarray


def get_run_totals(data: ExpRun, phase_map: PhaseMap) -> np.ndarray:
    grouped_data = get_run_by_phasemap_derive_sync(data, phase_map)
    return grouped_data[0]


def get_total_data() -> list[TotalData]:
    data = load_data()
    phase_map = get_phase_map_tot()

    all_nranks = [d['nranks'] for d in data]
    all_totals = [get_run_totals(d, phase_map) for d in data]

    tot_data = [
        TotalData(nranks=r, totals=t) for r, t in zip(all_nranks, all_totals)
    ]
    return tot_data


def get_policy_names() -> list[str]:
    data = load_data()
    orig_names = data[0]["policies"]
    mapped_names = [PolicyNameMap[o] for o in orig_names]
    return mapped_names


def get_annotation_points(
        tot_data: list[TotalData]) -> list[tuple[int, float, str]]:
    # (x, y, val)
    annot_points = []

    for lid, d in enumerate(tot_data):
        totals = d['totals']
        ratios = totals / totals[0]
        print(ratios)

        for x, (t, r) in enumerate(zip(totals, ratios)):
            # fmt ratios as pct with 0 decimal places
            annot_points.append((lid, x, int(t), f'{r:.0%}'))

    return annot_points


def add_annotations(ax):
    annot0 = [
        (0, 0, 8458, '100%'),
        (0, 1, 7430, '88%'),
        (0, 2, 7241, '86%'),
        (0, 3, 7163, '85%'),
        (0, 4, 7240, '86%'),
        (0, 5, 7357, '87%'),
    ]
    annot1 = [
        (1, 0, 12764, '100%'),
        (1, 1, 10770, '84%'),
        (1, 2, 10671, '84%'),
        (1, 3, 10452, '82%'),
        (1, 4, 10604, '83%'),
        (1, 5, 10905, '85%'),
    ]
    annot2 = [(2, 0, 9719, '100%'), (2, 1, 8039, '83%'), (2, 2, 7739, '80%'),
              (2, 3, 7712, '79%'), (2, 4, 7737, '80%'), (2, 5, 8049, '83%')]
    annot3 = [(3, 0, 12403, '100%'), (3, 1, 10311, '83%'), (3, 2, 9924, '80%'),
              (3, 3, 9730, '78%'), (3, 4, 9748, '79%'), (3, 5, 10352, '83%')]

    annots = annot0 + annot1 + annot2 + annot3

    for (l, x, y, val) in annots:
        if l in [1, 2]:  # skip 1024 and 2048 ranks
            continue
        # shifts for main() plot
        shifts = [-0.08, 0.02, 0.03, -0.06]

        # new shifts for main2 plot
        shifts = [-0.2, 0.04, 0.03, 0.07]
        val = val[:-1] + '\%'
        y = y * (1 + shifts[l])
        xypt = (x, y)
        xyt_pt = (0, shifts[l])
        ax.annotate(val,
                    xy=xypt,
                    xytext=xyt_pt,
                    textcoords='offset points',
                    fontsize=14)


def main():
    init()
    plt.close("all")

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.0))
    tot_data = get_total_data()
    ax.clear()

    markers = ['o', 'v', '^', 's']
    for lid, d in enumerate(tot_data):
        if lid in [1, 2]:  # skip 1024 and 2048 ranks
            continue
        nranks = d['nranks']
        totals = d['totals']

        ax.plot(totals, label=f"{nranks} ranks", marker=markers[lid])

    ax.set_ylim(bottom=0)

    policy_names = get_policy_names()
    ax.set_xticks(np.arange(len(policy_names)))
    ax.set_xticklabels(policy_names)
    #ax.legend(ncols=4)
    fig.legend(ncols=2,
               loc="outside upper center",
               columnspacing=1.5,
               handlelength=1.5,
               bbox_to_anchor=(0.55, 1.02))

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x / 3600:.1f} h"))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1800))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(300))
    ax.grid(which='minor', color='#ddd')
    ax.set_ylabel(r"\textbf{Total Runtime (h)}")

    ax.set_ylim([0, 14400])
    ax.set_xlim([-0.5, 5.5])

    add_annotations(ax)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85)

    # get all artists
    ax.get_children()

    # Only 2 lines now (512 and 4096)
    sb = StagedBuildout(ax, fig, "tot_runtime")

    # Line 0 (512): line + 6 annotations = indices 0, 2-7
    # Line 1 (4096): line + 6 annotations = indices 1, 8-13
    all_alx = [[[0, 2, 3, 4, 5, 6, 7], [], []],
               [[1, 8, 9, 10, 11, 12, 13], [], []]]

    for alx in all_alx:
        sb.disable_alx(*alx)

    c.save_plot(fig, "tot_runtime.f0")

    for idx, alx in enumerate(all_alx):
        sb.enable_alx(*alx)
        c.save_plot(fig, f"tot_runtime.f{idx+1}")

    plt.close("all")


def run_plot_runtime_baseline_only():
    all_rundata = load_data()
    phase_map = get_phase_map_tot()

    all_mapped = [
        get_run_by_phasemap_derive_sync(rd, phase_map) for rd in all_rundata
    ]
    all_baseline = [np.array(gd)[:, 0] for gd in all_mapped]
    all_ranks = [rd['nranks'] for rd in all_rundata]
    all_baseline = np.array(all_baseline)
    phases = phase_map['order']
    pcolors = [phase_map['colors'][p] for p in phases]
    totals = all_baseline[:, 0]

    init()
    plt.close("all")
    fig, ax = plt.subplots(figsize=(6.0, 6.5))

    bottom = np.zeros(all_baseline.shape[0])
    nphases = len(phases)
    data_x = list(range(len(all_ranks)))
    ax.clear()

    for pidx in list(range(1, nphases)):
        phase = phases[pidx]
        data = all_baseline[:, pidx]
        pcts = data / totals
        pcts_fmt = [f"{x*100:.1f}\%" for x in pcts]
        print(pcts_fmt)

        color = pcolors[pidx]
        bglob = ax.bar(data_x,
                       data,
                       bottom=bottom,
                       color=lighten_color(color, 0.5),
                       edgecolor='black',
                       linewidth=1,
                       width=0.75,
                       label=phase)
        if pidx == 4:
            label_type = 'edge'
        else:
            label_type = 'center'

        ax.bar_label(bglob,
                     labels=pcts_fmt,
                     label_type=label_type,
                     fontsize=18,
                     padding=1)
        bottom += data

    ax.set_xticks(data_x)
    ax.set_xticklabels(all_ranks, fontsize=18)
    # set y label fontsize to 18
    ax.yaxis.set_tick_params(labelsize=18)
    ax.set_xlabel("Number of Ranks", fontsize=18)
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/3600:.1f}h"))
    ax.set_ylabel("Time (hours)", fontsize=18)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1800))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    fig.tight_layout()
    fig.subplots_adjust(top=0.88)

    l.remove()
    l = ax.legend(ncols=2, loc="upper center", bbox_to_anchor=(0.5, 1.16))

    ax.get_children()
    all_alx = [[[1, 5, 9, 13, 17, 21, 25, 29], [], []],
               [[2, 6, 10, 14, 18, 22, 26, 30], [], []],
               [[3, 7, 11, 15, 19, 23, 27, 31], [], []]]

    sb = StagedBuildout(ax, fig, "runtime_baseline_only")
    sb.disable_alx(*all_alx[1])
    sb.enable_alx(*all_alx[1])

    alx = [[1, 5, 9, 13, 17, 21, 25, 29], [], []]
    sb.disable_alx(*alx)
    sb.enable_alx(*alx)

    for alx in all_alx:
        sb.disable_alx(*alx)

    frame_idx = 0
    c.save_plot(fig, f"runtime_baseline_only.f{frame_idx}")

    for idx, alx in enumerate(all_alx):
        sb.enable_alx(*alx)
        frame_idx += 1
        c.save_plot(fig, f"runtime_baseline_only.f{frame_idx}")

    plt.close("all")


def main2():
    init()
    plt.close("all")

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.8))
    tot_data = get_total_data()
    ax.clear()

    markers = ['o', 'v', '^', 's']
    for lid, d in enumerate(tot_data):
        nranks = d['nranks']
        totals = d['totals']

        ax.plot(totals, label=f"{nranks} ranks", marker=markers[lid])

    ax.set_ylim(bottom=0)

    policy_names = get_policy_names()
    ax.set_xticks(np.arange(len(policy_names)))
    ax.set_xticklabels(policy_names)
    #ax.legend(ncols=4)
    fig.legend(ncols=2,
               loc="outside upper center",
               columnspacing=0.5,
               bbox_to_anchor=(0.55, 0.45))

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x / 3600:.1f} h"))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(3600))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(600))
    ax.grid(which='minor', color='#ddd')
    ax.set_ylabel(r"\textbf{Total Runtime (h)}")

    ax.set_ylim([0, 14400])
    ax.set_xlim([-0.5, 5.5])

    add_annotations(ax)
    fig.tight_layout()
    #fig.subplots_adjust(top=0.8)

    c.save_plot(fig, "tot_runtime_all_half")

    plt.close("all")



if __name__ == "__main__":
    main()
    #main2()
