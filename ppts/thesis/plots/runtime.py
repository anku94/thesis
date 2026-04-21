import os
import json

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib.gridspec import GridSpec

import numpy as np

import common as c
from common import COLORS, PlotSaver, set_colormap
from typing import TypedDict

STYLE_FILE = c.get_plotsrc_dir() / "ppt.mplstyle"
"""
Func mapping:

all_funcs: list[FuncSpec] = [
    ("Driver_Main", "Total"),
    ("ConToPrim::Solve", "Comp"), ("CalculateFluxes", "Comp"),
    ("ApplyFloors", "Comp"),
    ("Task_SetInternalBoundaries", "Comp"),
    ("TmunuSourceTerms", "Comp"),
    ("WeightedSumData", "Comp"),
    ("UpdateMeshBlockTree", "CSync"),
    ("RedistributeAndRefineMeshBlocks", "LB::RNRMB"),
    ("Task_LoadAndSendBoundBufs", "Comm"),
    ("Task_ReceiveBoundBufs", "Comm"),
    ("MPI_Comm_dup", "DSync"),
    ("TaskRegion::CheckAndUpdate", "TSync"),
    ("parfor_Reconstruct", "Comp"),
    ("MPI_Allreduce", "RSync"),
    ("MPI_Iallgather_Async", "ISync"),
]

Color mapping:
    Compute: C0 (Green)
    Sync: C2 (Purple)
    Send: C1 (Red-ish)
    Recv: C3 (Pink-ish)
    Rebalance: C6?

"""


class ExpRun(TypedDict):
    name: str
    nranks: int
    policies: list[str]
    comp_phases: dict[str, list]
    comm_stats: dict[str, list]


class PhaseMap(TypedDict):
    mapping: dict[str, list[str]]
    order: list[str]
    colors: dict[str, str]


PolicyNameMap = {
    "baseline": "Baseline",
    "cdpc512par8": "X=0",
    "hybrid25": "X=25",
    "hybrid50": "X=50",
    "hybrid75": "X=75",
    "lpt": "X=100"
}


def init():
    plt.style.use(STYLE_FILE)
    plt.rcParams["axes.titlesize"]
    set_colormap("Pastel1-Dark")


def get_data_dir() -> str:
    return str(c.get_plotdata_dir())


def lighten_color(color, amount=0.5):
    rgb = mcolors.to_rgb(color)
    return tuple((1 - amount) * np.array(rgb) + amount)


def gen_random_run() -> ExpRun:
    dinit = np.array([2, 3, 2, 1])
    dcompute = np.array([10, 11, 9, 12])
    dfinalize = np.array([1, 2, 3, 4])

    return {
        "name": "random",
        "nranks": 512,
        "policies": ["a", "b", "c", "d"],
        "phases": {
            "init_1": dinit,
            "compute_1": dcompute,
            "finalize_1": dfinalize
        },
    }


def gen_random_phase_map() -> PhaseMap:
    return {
        "mapping": {
            "main": ["compute_1"],
            "others": ["init_1", "finalize_1"],
        },
        "order": ["main", "others"],
        "colors": {
            "main": "C0",
            "others": "C1",
        },
    }


def get_phase_map_tot() -> PhaseMap:
    return {
        "mapping": {
            "Total": ["Total"],
            "Compute": ["Comp"],
            "Communication": ["Comm"],
            "Synchronization": ["CSync", "DSync", "TSync", "RSync", "ISync"],
            "Rebalancing": ["LB::RNRMB"],
        },
        "order": [
            "Total", "Compute", "Communication", "Synchronization",
            "Rebalancing"
        ],
        "colors": {
            "Total": "C9",  # not used
            "Compute": COLORS["compute"],
            "Communication": COLORS["comm"],
            "Synchronization": COLORS["sync"],
            "Rebalancing": COLORS["rebalance"],
        },
    }


def get_phase_map_tradeoff() -> PhaseMap:
    return {
        "mapping": {
            "Total": ["Total"],
            "Compute": ["Comp"],
            "Communication": ["Comm"],
            "Sync": ["CSync", "DSync", "TSync", "RSync", "ISync"],
            "Rebalance": ["LB::RNRMB"],
        },
        "order": ["Communication", "Sync"],
        "colors": {
            "Total": "C9",  # not used
            "Compute": COLORS["compute"],
            "Communication": COLORS["comm"],
            "Sync": COLORS["sync"],
            "Rebalance": COLORS["rebalance"],
        },
    }


def get_run_by_phasemap(run_data: ExpRun,
                        phase_map: PhaseMap) -> list[np.ndarray]:
    all_phase_data: list[np.ndarray] = []

    for phase_group in phase_map["order"]:
        phases = phase_map["mapping"][phase_group]
        group_sum = np.sum(
            [run_data["comp_phases"][phase] for phase in phases], axis=0)

        group_avg = np.mean(group_sum)
        if group_avg > 1e6:
            print("Assuming time is in us, truncating")
            group_sum = np.array(group_sum / 1e6, dtype=np.int32)

        all_phase_data.append(group_sum)

    return all_phase_data


def get_run_by_phasemap_derive_sync(run_data: ExpRun,
                                    phase_map: PhaseMap) -> list[np.ndarray]:
    all_phase_data = get_run_by_phasemap(run_data, phase_map)
    # assert that order is
    expected_order = [
        "Total", "Compute", "Communication", "Synchronization", "Rebalancing"
    ]

    print(f"Phase order: {phase_map['order']}")
    print(f"Expected order: {expected_order}")

    given_order = phase_map["order"]
    assert given_order == expected_order

    nonsync_time = all_phase_data[1] + all_phase_data[2] + all_phase_data[4]
    estimated_sync_time = all_phase_data[0] - nonsync_time

    new_phase_data = [
        all_phase_data[0], all_phase_data[1], all_phase_data[2],
        estimated_sync_time, all_phase_data[4]
    ]
    return new_phase_data


def shift_bar_labels(bar_group, bar_labels, shift: float):
    extra = -0.8
    for idx, (bar, label) in enumerate(zip(bar_group, bar_labels)):
        cur_shift = shift + idx * extra
        label.set_x(bar.get_x() + cur_shift)


def load_data() -> list[ExpRun]:
    data_dir = get_data_dir()
    data_fpath = f"{data_dir}/blastwave_20241231.json"

    with open(data_fpath, "r") as f:
        data = json.load(f)

    all_runs = data["runs"]
    runs_str = ", ".join(all_runs)
    print(f"Loaded data for runs: {runs_str}")

    all_rundata: list[ExpRun] = [data["run_data"][k] for k in all_runs]

    return all_rundata


def plot_exp_runtime(ax, run_data: ExpRun, phase_map: PhaseMap, stack: bool):
    grouped_data = get_run_by_phasemap_derive_sync(run_data, phase_map)
    x = np.arange(len(run_data["policies"]))
    width = 0.44

    data_prev = None
    bottom = None

    for i, data in enumerate(grouped_data):
        if i == 0: continue

        phase_name = phase_map["order"][i]
        phase_color = phase_map["colors"][phase_name]

        print(f"Phase {phase_name} color: {phase_color}")

        if stack:
            barx = x + width / 2
            bottom = data_prev
        else:
            barx = x + i * width
            bottom = None

        bar_group = ax.bar(
            barx,
            data,
            width,
            bottom=bottom,
            label=phase_map["order"][i],
            color=lighten_color(phase_color, 0.5),
            edgecolor="black",
            linewidth=1,
            zorder=5,
        )
        if data_prev is None:
            data_prev = data
        else:
            data_prev += data

    # bar_total = np.sum(grouped_data, axis=0)
    bar_total = grouped_data[0]
    bar_rel = bar_total / bar_total[0]
    labels_abs = [f"{d:.0f}" for d in bar_total]
    labels_rel = [f"{d*100:.1f}\%" for d in bar_rel]
    labels_rel
    bar_total

    bar_labels = ax.bar_label(
        bar_group,
        labels=labels_rel,
        label_type="edge",
        fontsize=12,
        padding=1,
    )

    for label in bar_labels:
        label.set_bbox(dict(facecolor="white", alpha=0.5, edgecolor="white"))
        label.set_zorder(3)

    ax.set_xticks(x + width / 2)
    policies = run_data["policies"]
    policies_mapped = [PolicyNameMap[p] for p in policies]
    ax.set_xticklabels(policies_mapped)

    titlefontsz = plt.rcParams["axes.titlesize"]

    nranks = run_data["nranks"]
    ax_title = f"{nranks} Ranks"
    ax.set_title(ax_title, fontsize=titlefontsz - 2)
    ax.set_ylabel("Time (s)")

    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_axisbelow(True)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(3600))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(900))
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/3600:.0f}h"))

    ymax = ax.get_ylim()[1]
    ymax_unit = 3600 * 4
    # ylim should be a multiple of ymax_unit
    ylim = ymax_unit * np.ceil(ymax / ymax_unit) * 1.05  # 2% bonus
    ax.set_ylim(0, ylim)


def plot_exp_tradeoff(ax, run_data: ExpRun, phase_map: PhaseMap, stack: bool):
    grouped_data = get_run_by_phasemap(run_data, phase_map)
    x = np.arange(len(run_data["policies"]))
    width = 0.41
    data_prev = None
    bottom = None

    for i, data in enumerate(grouped_data):
        phase_name = phase_map["order"][i]
        phase_color = phase_map["colors"][phase_name]

        print(f"Phase {phase_name} color: {phase_color}")

        if stack:
            barx = x + width / 2
            bottom = data_prev
        else:
            barx = x + i * width
            bottom = None

        bar_group = ax.bar(
            barx,
            data,
            width,
            bottom=bottom,
            label=phase_map["order"][i],
            color=lighten_color(phase_color, 0.5),
            edgecolor="black",
            linewidth=1,
            zorder=5,
        )
        if data_prev is None:
            data_prev = data
        else:
            data_prev += data

        data_rel = data / data[0]
        labels_rel = [f"{d*100:.0f}\%" for d in data_rel]

        bar_labels = ax.bar_label(
            bar_group,
            labels=labels_rel,
            label_type="edge",
            fontsize=10,
            padding=1,
        )

        for label in bar_labels:
            label.set_bbox(
                dict(facecolor="white", alpha=0.1, edgecolor="white"))
            label.set_zorder(3)

        if i == 0:
            shift_bar_labels(bar_group, bar_labels, -3)
        elif i == 1:
            shift_bar_labels(bar_group, bar_labels, 1)

    ax.set_xticks(x + width / 2)
    policies = run_data["policies"]
    policies_mapped = [PolicyNameMap[p] for p in policies]

    titlefontsz = plt.rcParams["axes.titlesize"]
    xticklabelsz = plt.rcParams["xtick.labelsize"]
    yticklabelsz = plt.rcParams["ytick.labelsize"]

    ax.set_xticklabels(policies_mapped, fontsize=xticklabelsz - 0)
    ax.yaxis.set_tick_params(labelsize=yticklabelsz - 0)

    nranks = run_data["nranks"]
    ax_title = f"{nranks} Ranks"
    ax.set_title(ax_title, fontsize=titlefontsz - 2)
    # ax.set_ylabel("Time (s)")

    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_axisbelow(True)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1800))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(300))
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/60:.0f}m"))

    # ymax = ax.get_ylim()[1]
    # ymax_unit = 3600 * 4
    # # ylim should be a multiple of ymax_unit
    # ylim = ymax_unit * np.ceil(ymax / ymax_unit)
    # ax.set_ylim(0, ylim)


def plot_exp_tradeoff_wide(axl, axr, run_data: ExpRun, phase_map: PhaseMap,
                           stack: bool):
    # grouped_data = get_run_by_phasemap(run_data, phase_map)
    grouped_data = get_run_by_phasemap_derive_sync(run_data, phase_map)
    x = np.arange(len(run_data["policies"]))
    width = 0.41
    data_prev = None
    bottom = None

    for i, data in enumerate(grouped_data):
        phase_name = phase_map["order"][i]
        phase_color = phase_map["colors"][phase_name]

        print(f"Phase {phase_name} color: {phase_color}")

        if i == 2: ax = axl
        elif i == 3: ax = axr
        else: continue

        if stack:
            barx = x + width / 2
            bottom = data_prev
        else:
            barx = x + (i - 2) * width
            bottom = None

        bar_group = ax.bar(
            barx,
            data,
            width,
            bottom=bottom,
            label=phase_map["order"][i],
            color=lighten_color(phase_color, 0.5),
            edgecolor="black",
            linewidth=1,
            zorder=5,
        )
        if data_prev is None: data_prev = data
        else: data_prev += data

        data_rel = data / data[0]
        labels_rel = [f"{d*100:.0f}\%" for d in data_rel]

        bar_labels = ax.bar_label(
            bar_group,
            labels=labels_rel,
            label_type="edge",
            fontsize=9,
            padding=1,
            rotation=60,
        )

        for label in bar_labels:
            label.set_bbox(
                dict(facecolor="white", alpha=0.1, edgecolor="white"))
            label.set_zorder(3)
            # label.set_x(label.get_position()[0] + 0.9)

        if i == 2: shift_bar_labels(bar_group, bar_labels, 1)
        elif i == 3: shift_bar_labels(bar_group, bar_labels, 2)

    ax = axl

    ax.set_xticks(x + width / 2)
    policies = run_data["policies"]
    policies_mapped = [PolicyNameMap[p] for p in policies]

    titlefontsz = plt.rcParams["axes.titlesize"]
    xticklabelsz = plt.rcParams["xtick.labelsize"]
    yticklabelsz = plt.rcParams["ytick.labelsize"]

    ax.set_xticklabels(policies_mapped, fontsize=xticklabelsz - 3)
    ax.yaxis.set_tick_params(labelsize=yticklabelsz - 0)

    nranks = run_data["nranks"]
    ax_title = f"{nranks} Ranks"
    ax.set_title(ax_title, fontsize=titlefontsz - 8)
    # ax.set_ylabel("Time (s)")

    ax = axl
    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    axl.set_axisbelow(True)
    axr.set_axisbelow(True)

    axl.yaxis.set_major_locator(ticker.MultipleLocator(600))
    axl.yaxis.set_minor_locator(ticker.MultipleLocator(300))
    axl.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/60:.0f}m"))
    axl.set_ylim(0, 1800)
    #
    axr.yaxis.set_major_locator(ticker.MultipleLocator(3600))
    axr.yaxis.set_minor_locator(ticker.MultipleLocator(1200))
    axr.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/60:.0f}m"))
    axr.set_ylim(0, 7200)

    axl.set_ylim(0, 2100)
    axr.set_ylim(0, 8400)

    axr.grid(False)

    # ymax = ax.get_ylim()[1]
    # ymax_unit = 3600 * 4
    # # ylim should be a multiple of ymax_unit
    # ylim = ymax_unit * np.ceil(ymax / ymax_unit)
    # ax.set_ylim(0, ylim)


def run_plot_runtime():
    init()
    all_rundata = load_data()
    phase_map = get_phase_map_tot()

    figsize = (9, 4.5)
    fig, axes = plt.subplots(2, 2, figsize=figsize, layout="constrained")
    # fig.clear()
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    # axes = fig.subplots(2, 2)
    [[ax0, ax1], [ax2, ax3]] = axes

    [ax.clear() for ax in axes.flat]
    plot_exp_runtime(ax0, all_rundata[0], phase_map, stack=True)
    plot_exp_runtime(ax1, all_rundata[1], phase_map, stack=True)
    plot_exp_runtime(ax2, all_rundata[2], phase_map, stack=True)
    plot_exp_runtime(ax3, all_rundata[3], phase_map, stack=True)

    handles, labels = ax0.get_legend_handles_labels()
    legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)

    ax0.set_xticklabels([])
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax3.set_yticklabels([])
    ax0.set_xlabel("")
    ax1.set_xlabel("")
    ax1.set_ylabel("")
    ax3.set_ylabel("")
    ax0.set_ylabel("")
    ax2.set_ylabel("")
    fig.supylabel("Time (s)", fontsize=18)
    # legend.remove()
    # plt.show()
    # plt.close("all")

    plot_fname = "blastwave_runtime"
    PlotSaver.save(fig, "", None, plot_fname)


def run_plot_runtime_wide():
    init()
    plt.close("all")

    all_rundata = load_data()
    phase_map = get_phase_map_tot()

    all_rundata[3]

    # plt.close("all")

    figsize = (15, 3.0)
    # fig, axes = plt.subplots(2, 2, figsize=figsize, layout="constrained")
    fig, axes = plt.subplots(1, 4, figsize=figsize, layout="constrained")
    # fig.clear()
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    # axes = fig.subplots(2, 2)
    # [[ax0, ax1], [ax2, ax3]] = axes
    ax0, ax1, ax2, ax3 = axes

    ax = ax0
    run_data = all_rundata[0]

    [ax.clear() for ax in axes.flat]
    stack = True
    plot_exp_runtime(ax0, all_rundata[0], phase_map, stack=True)
    plot_exp_runtime(ax1, all_rundata[1], phase_map, stack=True)
    plot_exp_runtime(ax2, all_rundata[2], phase_map, stack=True)
    plot_exp_runtime(ax3, all_rundata[3], phase_map, stack=True)

    handles, labels = ax0.get_legend_handles_labels()
    legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)

    ax1.set_ylabel("")
    ax2.set_ylabel("")
    ax3.set_ylabel("")

    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax3.set_yticklabels([])

    ax0.set_ylabel("Time", ha='center', va='bottom', rotation=0, fontsize=18)
    ax0.yaxis.set_label_coords(-0.09, 1.09)

    # reduce fontsize of xticklabels by 1 pt
    xticklabelsz = plt.rcParams["xtick.labelsize"]
    ax0.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 3)
    ax1.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 3)
    ax2.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 3)
    ax3.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 3)

    # reduce titlesize by 2 pt
    titlefontsz = plt.rcParams["axes.titlesize"]
    ax0.set_title(ax0.get_title(), fontsize=titlefontsz - 4)
    ax1.set_title(ax1.get_title(), fontsize=titlefontsz - 4)
    ax2.set_title(ax2.get_title(), fontsize=titlefontsz - 4)
    ax3.set_title(ax3.get_title(), fontsize=titlefontsz - 4)

    # legend.remove()
    # plt.show()
    # plt.close("all")

    plot_fname = "blastwave_runtime_wide"
    PlotSaver.save(fig, "", None, plot_fname)


"""
run_plot_runtime_wide_mini: wide version, but just 512 and 4096
abandoned... we don't need runtime wide mini
"""


def run_plot_runtime_wide_mini():
    init()
    plt.close("all")
    all_rundata = load_data()
    phase_map = get_phase_map_tot()
    figsize = (7.4, 3.0)

    fig, axes = plt.subplots(1, 2, figsize=figsize, layout="constrained")
    # fig.clear()
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)
    ax0, ax1 = axes

    [ax.clear() for ax in axes]
    stack = True
    plot_exp_runtime(ax0, all_rundata[0], phase_map, stack=stack)
    plot_exp_runtime(ax1, all_rundata[3], phase_map, stack=stack)

    handles, labels = ax0.get_legend_handles_labels()
    legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)

    ax1.set_ylabel("")
    ax1.set_yticklabels([])

    ax0.set_ylabel("Time", ha='center', va='bottom', rotation=0, fontsize=18)
    ax0.yaxis.set_label_coords(-0.09, 1.09)
    pass


def run_plot_tradeoff():
    all_rundata = load_data()
    # phase_map = get_phase_map_tradeoff()
    phase_map = get_phase_map_tot()

    plt.close("all")
    figsize = (9, 3.5)
    fig, axes = plt.subplots(2, 2, figsize=figsize, layout="constrained")
    # fig.clear()
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)
    # plt.draw()

    # axes = fig.subplots(2, 2)
    [[ax0, ax1], [ax2, ax3]] = axes

    [ax.clear() for ax in axes.flat]
    plot_exp_tradeoff(ax0, all_rundata[0], phase_map, stack=False)
    plot_exp_tradeoff(ax1, all_rundata[1], phase_map, stack=False)
    plot_exp_tradeoff(ax2, all_rundata[2], phase_map, stack=False)
    plot_exp_tradeoff(ax3, all_rundata[3], phase_map, stack=False)

    ax0.set_xticklabels([])
    ax1.set_xticklabels([])
    ax1.set_ylabel("")
    ax3.set_ylabel("")
    ax0.set_ylabel("")
    ax2.set_ylabel("")

    ax1.set_yticklabels([])
    ax3.set_yticklabels([])
    fig.supylabel("Time (s)", fontsize=18)
    fig.supylabel("")

    ax0.set_ylim(0, 7200 + 800)
    # ax1.set_ylim(0, 10800 + 600)
    ax1.set_ylim(0, 7200 + 800)
    ax2.set_ylim(0, 7200 + 800)
    ax3.set_ylim(0, 7200 + 800)

    handles, labels = ax0.get_legend_handles_labels()
    legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)

    ax0.set_ylabel("Time", ha='center', va='bottom', rotation=0, fontsize=18)
    ax0.yaxis.set_label_coords(-0.09, 1.09)

    plot_fname = "blastwave_tradeoff"
    PlotSaver.save(fig, "", None, plot_fname)

    # handles, labels = ax0.get_legend_handles_labels()
    # legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)


def run_plot_tradeoff_wide(fig):
    all_rundata = load_data()
    # phase_map = get_phase_map_tradeoff()
    phase_map = get_phase_map_tot()

    # fig = plt.figure(figsize=(15, 2.2), constrained_layout=True)
    fig.clear()

    # constrained_layout does not allow subplots_adjust, this circumvents that
    engine = fig.get_layout_engine()
    engine.set(rect=(0.0, 0.0, 1.0, 0.94))
    fig.canvas.draw()

    gs = GridSpec(1, 4, figure=fig)
    axes = [fig.add_subplot(gs[0, i]) for i in range(4)]
    ax0, ax1, ax2, ax3 = axes

    # plt.close("all")
    # figsize = (15, 2.0)
    # fig, axes = plt.subplots(1, 4, figsize=figsize, layout="constrained")
    # fig.clear()
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)
    # plt.draw()

    # axes = fig.subplots(1, 4)
    # ax0, ax1, ax2, ax3 = axes

    ax0t = ax0.twinx()
    ax1t = ax1.twinx()
    ax2t = ax2.twinx()
    ax3t = ax3.twinx()

    all_axes = [ax0, ax0t, ax1, ax1t, ax2, ax2t, ax3, ax3t]
    [ax.clear() for ax in all_axes]

    plot_exp_tradeoff_wide(ax0, ax0t, all_rundata[0], phase_map, stack=False)
    plot_exp_tradeoff_wide(ax1, ax1t, all_rundata[1], phase_map, stack=False)
    plot_exp_tradeoff_wide(ax2, ax2t, all_rundata[2], phase_map, stack=False)
    plot_exp_tradeoff_wide(ax3, ax3t, all_rundata[3], phase_map, stack=False)

    for ax in all_axes[1:-1]:
        # clear yticks
        ax.set_yticklabels([])

    h0, l0 = ax0.get_legend_handles_labels()
    h0t, l0t = ax0t.get_legend_handles_labels()

    legend_fontsz = plt.rcParams["legend.fontsize"]
    legend = fig.legend(h0 + h0t,
                        l0 + l0t,
                        loc="outside upper center",
                        ncol=4,
                        bbox_to_anchor=(0.5, 1.01),
                        fontsize=legend_fontsz - 1)
    # delete legend

    ylabelsz = plt.rcParams["axes.labelsize"]
    ax0.set_ylabel("Comm. Time", fontsize=ylabelsz - 2)
    ax3t.set_ylabel("Sync. Time", fontsize=ylabelsz - 2)

    yticklabelsz = plt.rcParams["ytick.labelsize"]
    ax0.yaxis.set_tick_params(labelsize=yticklabelsz - 2)
    ax3t.yaxis.set_tick_params(labelsize=yticklabelsz - 2)

    # make 3t label appear on the right side
    ax3t.yaxis.set_label_position("right")

    titlefontsz = plt.rcParams["axes.titlesize"]

    ax0.set_title(ax0.get_title(), loc='left', fontsize=titlefontsz - 4)
    ax1.set_title(ax1.get_title(), loc='left', fontsize=titlefontsz - 4)
    ax2.set_title(ax2.get_title(), loc='right', fontsize=titlefontsz - 4)
    ax3.set_title(ax3.get_title(), loc='right', fontsize=titlefontsz - 4)

    xticklabelsz = plt.rcParams["xtick.labelsize"]
    ax0.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 4)
    ax1.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 4)
    ax2.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 4)
    ax3.set_xticklabels(ax0.get_xticklabels(), fontsize=xticklabelsz - 4)

    ax0.set_title("")
    ax1.set_title("")
    ax2.set_title("")
    ax3.set_title("")

    # plot_fname = "blastwave_tradeoff_wide"
    # PlotSaver.save(fig, "", None, plot_fname)

    # handles, labels = ax0.get_legend_handles_labels()
    # legend = fig.legend(handles, labels, loc="outside upper center", ncol=4)


"""
run_plot_tradeoff_wide_mini: wide version, but just 512 and 4096
"""


def run_plot_tradeoff_wide_mini():
    plt.close("all")
    init()
    all_rundata = load_data()
    phase_map = get_phase_map_tot()

    fig = plt.figure(figsize=(7.4, 2.2), constrained_layout=True)
    fig.clear()

    engine = fig.get_layout_engine()
    engine.set(rect=(0.0, 0.0, 1.0, 0.94))
    fig.canvas.draw()

    gs = GridSpec(1, 2, figure=fig)
    axes = [fig.add_subplot(gs[0, i]) for i in range(2)]
    ax0, ax1 = axes
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    ax0t = ax0.twinx()
    ax1t = ax1.twinx()

    all_axes = [ax0, ax0t, ax1, ax1t]
    [ax.clear() for ax in all_axes]

    plot_exp_tradeoff_wide(ax0, ax0t, all_rundata[0], phase_map, stack=False)
    plot_exp_tradeoff_wide(ax1, ax1t, all_rundata[3], phase_map, stack=False)

    # delete intermediate yaxis labels
    ax0t.set_yticklabels([])
    ax1.set_yticklabels([])

    # set up yaxis labels
    ylabelsz = plt.rcParams["axes.labelsize"]
    ax0.set_ylabel("Comm. Time", fontsize=ylabelsz - 2)
    ax1t.set_ylabel("Sync. Time", fontsize=ylabelsz - 2)
    ax1t.yaxis.set_label_position("right")  # make it appear on right

    # set up axis titles on left and right
    titlefontsz = plt.rcParams["axes.titlesize"]
    ax0.set_title(ax0.get_title(), loc='left', fontsize=titlefontsz - 5)
    ax1.set_title(ax1.get_title(), loc='right', fontsize=titlefontsz - 5)

    # set up xticklabelsz
    xticklabelsz = plt.rcParams["xtick.labelsize"]
    for ax in [ax0, ax1]:
        ax.set_title("")
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=xticklabelsz - 6)

    # set up yticklabelsz
    yticklabelsz = plt.rcParams["ytick.labelsize"]
    for ax in [ax0, ax1t]:
        ax.yaxis.set_tick_params(labelsize=yticklabelsz - 2)

    # setup ylabel size
    ylabelsz = plt.rcParams["axes.labelsize"]
    for ax in [ax0, ax1t]:
        ax.set_ylabel(ax.get_ylabel(), fontsize=ylabelsz - 2)

    # setup legend
    h0, l0 = ax0.get_legend_handles_labels()
    h0t, l0t = ax0t.get_legend_handles_labels()
    legend_fontsz = plt.rcParams["legend.fontsize"]

    legend = fig.legend(h0 + h0t, ['P2P Comm.', 'Sync.'],
                        loc="outside upper center",
                        ncol=4,
                        bbox_to_anchor=(0.5, 1.01),
                        fontsize=legend_fontsz - 1)
    # legend.remove() # delete legend
    plot_fname = "blastwave_tradeoff_wide_mini"
    PlotSaver.save(fig, "", None, plot_fname)
    plt.close(fig)
    pass


def plot_exp_msgcnt(ax, run_data: ExpRun):
    msgcnt_local = run_data["comm_stats"]["msgcnt_local"]
    msgcnt_total = run_data["comm_stats"]["msgcnt_total"]

    msgcnt_local = np.array(msgcnt_local)
    msgcnt_total = np.array(msgcnt_total)
    msgcnt_remote = msgcnt_total - msgcnt_local

    norm_factor = msgcnt_total[0]
    msgcnt_locrel = msgcnt_local / norm_factor
    msgcnt_remrel = msgcnt_remote / norm_factor

    x = np.arange(len(run_data["policies"]))
    width = 0.75  # increased from 0.6 for wide_mini

    ax.clear()

    cur_cmap = plt.colormaps["Pastel1"]

    color_loc = lighten_color("C1", 0.5)
    color_loc = cur_cmap(2)
    color_rem = lighten_color("C2", 0.5)
    color_rem = cur_cmap(0)

    bar_loc = ax.bar(
        x,
        msgcnt_local,
        width,
        label="Local Message Count",
        color=color_loc,
        edgecolor="black",
        linewidth=1,
    )

    # set a translucent background for the labels to C1

    loc_label_text = [f"{d*100:.0f}\%" for d in msgcnt_locrel]
    loc_label_text[-3] += "↓"
    loc_label_text[-2] += "↓"
    loc_label_text[-1] += "↓"

    loc_labels = ax.bar_label(
        bar_loc,
        labels=loc_label_text,
        label_type="center",
        fontsize=11,
        padding=0,
    )

    # for label in loc_labels[-2:]:
    #     label.set_bbox(dict(facecolor="white", alpha=0.4, edgecolor="none"))

    loc_labels[-3].set_y(12)
    loc_labels[-2].set_y(9)
    loc_labels[-1].set_y(9)

    bar_glob = ax.bar(
        x,
        msgcnt_remote,
        width,
        bottom=msgcnt_local,
        label="Global Message Count",
        color=color_rem,
        edgecolor="black",
        linewidth=1,
    )

    ax_barlbls = [f"{d*100:.0f}\%" for d in msgcnt_remrel]
    ax.bar_label(bar_glob,
                 labels=ax_barlbls,
                 label_type="center",
                 fontsize=11,
                 padding=1)

    ax.set_xticks(x)
    policies = run_data["policies"]
    policies_mapped = [PolicyNameMap[p] for p in policies]
    ax.set_xticklabels(policies_mapped)

    titlefontsz = plt.rcParams["axes.titlesize"]

    nranks = run_data["nranks"]
    ax_title = f"{nranks} Ranks"
    ax.set_title(ax_title, fontsize=titlefontsz - 2)
    ax.set_ylabel("Message Count")

    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_axisbelow(True)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/1e9:.0f}B"))

    # ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(200))
    #
    # ymax = ax.get_ylim()[1]
    # ymax_unit = 10000
    # # ylim should be a multiple of ymax_unit
    # ylim = ymax_unit * np.ceil(ymax / ymax_unit) * 1.01  # 1% bonus
    # ax.set_ylim(0, ylim)
    #


def run_plot_comm():
    all_rundata = load_data()
    figsize = (9, 3.5)

    fig, axes = plt.subplots(2, 2, figsize=figsize, layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    fig.clear()
    axes = fig.subplots(2, 2)

    [[ax0, ax1], [ax2, ax3]] = axes

    [ax.clear() for ax in axes.flat]
    plot_exp_msgcnt(ax0, all_rundata[0])
    plot_exp_msgcnt(ax1, all_rundata[1])
    plot_exp_msgcnt(ax2, all_rundata[2])
    plot_exp_msgcnt(ax3, all_rundata[3])

    ax0.set_ylabel("Count", ha='center', va='bottom', rotation=0)
    ax0.yaxis.set_label_coords(-0.04, 1.03)

    ax0.set_xticklabels([])
    ax1.set_xticklabels([])
    ax1.set_ylabel("")
    ax3.set_ylabel("")
    ax0.set_ylabel("")
    ax2.set_ylabel("")
    fig.supylabel("Message Count", fontsize=18)
    fig.supylabel("")

    handles, labels = ax0.get_legend_handles_labels()
    legend = fig.legend(handles, labels, loc="outside upper center", ncol=2)

    plot_fname = "blastwave_comm"
    PlotSaver.save(fig, "", None, plot_fname)


def run_plot_comm_wide():
    all_rundata = load_data()
    figsize = (15, 2.2)

    fig = plt.figure(figsize=figsize, constrained_layout=True)
    fig.clear()

    # constrained_layout does not allow subplots_adjust, this circumvents that
    engine = fig.get_layout_engine()
    engine.set(rect=(0.0, 0.0, 1.0, 0.94))
    fig.canvas.draw()

    gs = GridSpec(1, 4, figure=fig)
    axes = [fig.add_subplot(gs[0, i]) for i in range(4)]
    ax0, ax1, ax2, ax3 = axes

    # fig, axes = plt.subplots(1, 4, figsize=figsize, layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    # fig.clear()
    # axes = fig.subplots(2, 2)

    # [[ax0, ax1], [ax2, ax3]] = axes
    # axes = fig.subplots(1, 4)
    # ax0, ax1, ax2, ax3 = axes

    # [ax.clear() for ax in axes.flat]
    plot_exp_msgcnt(ax0, all_rundata[0])
    plot_exp_msgcnt(ax1, all_rundata[1])
    plot_exp_msgcnt(ax2, all_rundata[2])
    plot_exp_msgcnt(ax3, all_rundata[3])

    ax0.set_ylabel("Message Count")
    # ax0.set_ylabel("Message Count", ha='center', va='bottom', rotation=0)
    # ax0.yaxis.set_label_coords(-0.04, 1.03)

    # ax0.set_xticklabels([])
    # ax1.set_xticklabels([])
    # ax0.set_ylabel("")
    ax1.set_ylabel("")
    ax2.set_ylabel("")
    ax3.set_ylabel("")
    #
    # fig.supylabel("Message Count", fontsize=18)
    # fig.supylabel("")

    handles, labels = ax0.get_legend_handles_labels()
    # legend = fig.legend(handles, labels, loc="outside upper center", ncol=2)
    labels = ['Local Count', 'Remote Count']
    legend = fig.legend(handles,
                        labels,
                        loc="outside upper center",
                        ncol=2,
                        bbox_to_anchor=(0.52, 1.01))
    # legend.remove()

    xticklabelsz = plt.rcParams["xtick.labelsize"]
    titlefontsz = plt.rcParams["axes.titlesize"]

    for ax in axes:
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=xticklabelsz - 4)
        ax.set_title(ax.get_title(), fontsize=titlefontsz - 4)

    # make ax1 title left-aligned
    ax0.set_title(ax0.get_title(), loc='left', fontsize=titlefontsz - 4)
    ax1.set_title(ax1.get_title(), loc='left', fontsize=titlefontsz - 4)
    ax2.set_title(ax2.get_title(), loc='right', fontsize=titlefontsz - 4)
    ax3.set_title(ax3.get_title(), loc='right', fontsize=titlefontsz - 4)

    ax0.set_title("")
    ax1.set_title("")
    ax2.set_title("")
    ax3.set_title("")

    plot_fname = "blastwave_comm_wide"
    PlotSaver.save(fig, "", None, plot_fname)


"""
run_plot_comm_wide_mini: wide version, but just 512 and 4096
"""


def run_plot_comm_wide_mini():
    all_rundata = load_data()
    figsize = (7.4, 2.2)

    fig = plt.figure(figsize=figsize, constrained_layout=True)
    fig.clear()

    engine = fig.get_layout_engine()
    engine.set(rect=(0.0, 0.0, 1.0, 0.94))
    fig.canvas.draw()

    gs = GridSpec(1, 2, figure=fig)
    axes = [fig.add_subplot(gs[0, i]) for i in range(2)]
    ax0, ax1 = axes
    fig.set_constrained_layout_pads(w_pad=0.06,
                                    h_pad=0.06,
                                    wspace=0.01,
                                    hspace=0.01)

    plot_exp_msgcnt(ax0, all_rundata[0])
    plot_exp_msgcnt(ax1, all_rundata[3])

    ax0.set_ylabel("Message Count")
    ax1.set_ylabel("")

    handles, labels = ax0.get_legend_handles_labels()
    labels = ['Local Count', 'Remote Count']
    legend = fig.legend(handles,
                        labels,
                        loc="outside upper center",
                        ncol=2,
                        bbox_to_anchor=(0.52, 1.01))

    # legend.remove()

    xticklabelsz = plt.rcParams["xtick.labelsize"]
    titlefontsz = plt.rcParams["axes.titlesize"]

    for ax in axes:
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=xticklabelsz - 4)
        ax.set_title(ax.get_title(), fontsize=titlefontsz - 4)

    # make ax1 title left-aligned
    ax0.set_title(ax0.get_title(), loc='left', fontsize=titlefontsz - 4)
    ax0.set_title("")

    ax1.set_title(ax1.get_title(), loc='right', fontsize=titlefontsz - 4)
    ax1.set_title("")

    plot_fname = "blastwave_comm_wide_mini"
    PlotSaver.save(fig, "", None, plot_fname)
    plt.close(fig)


def run_plot_runtime_baseline_only():
    all_rundata = load_data()
    phase_map = get_phase_map_tot()

    all_mapped = [
        get_run_by_phasemap_derive_sync(rd, phase_map) for rd in all_rundata
    ]
    all_baseline = [np.array(gd)[:, 0] for gd in all_mapped]
    all_ranks = [rd['nranks'] for rd in all_rundata]
    all_baseline = np.array(all_baseline)
    all_baseline

    phases = phase_map['order']
    pcolors = [phase_map['colors'][p] for p in phases]
    pcolors
    phases

    totals = all_baseline[:, 0]

    init()
    plt.close("all")
    fig, ax = plt.subplots(figsize=(6, 4))

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
                     fontsize=13,
                     padding=1)
        bottom += data

    ax.set_xticks(data_x)
    ax.set_xticklabels(all_ranks)
    ax.set_xlabel("Number of Ranks")
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x/3600:.1f}h"))
    ax.set_ylabel("Time (hours)")
    ax.yaxis.set_major_locator(ticker.MultipleLocator(3600))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.grid(which="major", axis="y", color="#bbb")
    ax.grid(which="minor", axis="y", color="#ddd")
    fig.tight_layout()

    pass


def run_print_stats():
    all_rundata = load_data()
    phase_map = get_phase_map_tot()
    keys = phase_map['order']
    keys

    cur_rundata = all_rundata[0]
    cur_phases = cur_rundata['comp_phases']
    tot = cur_phases['Total']
    comp = cur_phases['Comp']

    tot = (np.array(tot) / 1e6).astype(np.int32)
    comp = (np.array(comp) / 1e6).astype(np.int32)

    tot
    comp
    diff = tot - comp
    1 - (diff / diff[0])
    1 - (tot / tot[0])
    tot

    for cur_rundata in all_rundata:
        run_name = cur_rundata["name"]
        print(f'\nAnalyzing run: {run_name}')
        print('==========================')
        grouped_data = get_run_by_phasemap_derive_sync(cur_rundata, phase_map)
        group_sum = np.sum(grouped_data[1:], axis=0)

        for k, kdata in zip(keys, grouped_data):
            kdatapct = kdata / group_sum
            kdatapctstr = ', '.join([f"{x:5d}s" for x in kdata])
            kdatastrarr = []

            for kdabs, kdrel in zip(kdata, kdatapct):
                kdabsstr = f"{kdabs:5d}s"
                kdrelstr = f"{kdrel*100:.2f}%"
                # kdrelstr = f"{kdrelstr:6s}"
                kdstr = f"{kdabsstr} ({kdrelstr:6s})"
                kdatastrarr.append(kdstr)

            kdatastr = ','.join(kdatastrarr)
            print(f"{k:14s}: {kdatastr}")

    print('--------------------------')
    return

    all_rundata

    for cur_rundata in all_rundata:
        run_name = cur_rundata["name"]
        print(f'\nAnalyzing run: {run_name}')
        print('==========================')
        grouped_data = get_run_by_phasemap_derive_sync(cur_rundata, phase_map)
        print(grouped_data)
        non_comp_data = grouped_data[2:]
        non_comp_sum = np.sum(non_comp_data, axis=0)
        non_comp_rel = non_comp_sum / non_comp_sum[0]
        ncrel_str = [f"{x:.2%}" for x in non_comp_rel]
        print(f"Non-compute Time: ", ', '.join(ncrel_str))


if __name__ == "__main__":
    init()
    plt.close("all")

    # run_plot_runtime_wide()
    run_plot_tradeoff_wide_mini()
    run_plot_comm_wide_mini()

    # run_plot_runtime()
    # run_plot_tradeoff()
    # run_plot_comm()

    # run_print_stats()

    # run_plot_runtime_wide()
    #
    # fig = plt.figure(figsize=(15, 2.2), constrained_layout=True)
    # run_plot_tradeoff_wide(fig)
    # plot_fname = "blastwave_tradeoff_wide"
    # PlotSaver.save(fig, "", None, plot_fname)
    #
    # run_plot_comm_wide()
