from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.lines import Line2D

import common as c


def read_query_csvs(fpath: str):
    basedir = c.get_plotdata_dir()
    csv_path = basedir / "querylog.csv"

    fq_path = basedir / "20220328.queries.fastquery.aggr.csv"
    df_fq = pd.read_csv(fq_path)

    data = pd.read_csv(csv_path)
    data = data.sort_values("qselectivity")

    all_plfs = sorted(data["plfspath"].unique())
    type_carp = all_plfs[1]
    type_flat = all_plfs[0]

    print(type_carp)
    print(type_flat)

    assert not type_carp.endswith(".merged")
    assert type_flat.endswith(".merged")

    data.loc[data["plfspath"] == type_flat, "qsortus"] = 0
    data["qreadus"] += data["qsortus"]

    data["qreadus"] /= 1e6
    data["qkeyselectivity"] *= 100

    data_aggr = data.groupby(
        ["plfspath", "qbegin", "qend", "qkeyselectivity"], as_index=False
    ).agg({"qreadus": ["mean", "std"]})

    df_carp = data_aggr[data_aggr["plfspath"] == type_carp].copy()
    df_flat = data_aggr[data_aggr["plfspath"] == type_flat].copy()

    df_carp = pd.DataFrame(df_carp[["qbegin", "qend", "qkeyselectivity", "qreadus"]])
    df_flat = pd.DataFrame(df_flat[["qbegin", "qend", "qkeyselectivity", "qreadus"]])

    df_carp.sort_values("qbegin", inplace=True)
    df_flat.sort_values("qbegin", inplace=True)

    df_carp.rename(columns={"qkeyselectivity": "qsel", "qreadus": "time"}, inplace=True)
    df_flat.rename(columns={"qkeyselectivity": "qsel", "qreadus": "time"}, inplace=True)

    df_carp.columns = list(map("".join, df_carp.columns.values))
    df_flat.columns = list(map("".join, df_flat.columns.values))

    df_carp["selrat"] = np.array(df_carp["qsel"].tolist()) / np.array(
        df_fq["qsel"].tolist()
    )
    df_carp["qsel"] = df_fq["qsel"].tolist()
    df_flat["qsel"] = df_fq["qsel"].tolist()

    drop_idx = []
    keep_idx = [0, 4, 7, 15, 18, 21, 22, 24]
    drop_idx = [i for i in range(25) if i not in keep_idx]

    for df in [df_carp, df_flat, df_fq]:
        df.sort_values("qsel", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop([df.index[x] for x in drop_idx], inplace=True)

    scan_fpath = basedir / "querylog.scan.csv"
    df_scan = pd.read_csv(scan_fpath)
    df_scan["qreadus"] += df_scan["qsortus"]
    df_scan = df_scan[["qbegin", "qend", "qkeyselectivity", "qreadus"]]
    df_scan["qreadus"] /= 1e6
    df_scan["qkeyselectivity"] *= 100
    df_scan.rename(columns={"qkeyselectivity": "qsel", "qreadus": "time"}, inplace=True)
    df_scan["qsel"] = list(df_carp["qsel"])

    with pd.option_context("display.float_format", "{:,.2f}".format):
        print(df_carp)
        print(df_flat)
        print(df_fq)
        print(df_scan)

    return df_carp, df_flat, df_fq, df_scan


def get_legend_items(all_colors: list[str]) -> list:
    legend_items = []
    legend_items.append(
        Line2D(
            [0],
            [0],
            marker="s",
            mfc=all_colors[3],
            label="DeltaFS/FullScan",
            mec="black",
            markersize=12,
            linestyle="None",
        )
    )

    legend_items.append(
        Line2D(
            [0],
            [0],
            marker="^",
            mfc=all_colors[2],
            mec="black",
            label="FastQuery",
            markersize=12,
            linestyle="None",
        )
    )

    legend_items.append(
        Line2D(
            [0],
            [0],
            marker="D",
            mfc=all_colors[1],
            mec="black",
            label="TritonSort",
            markersize=12,
            linestyle="None",
        )
    )

    legend_items.append(
        Line2D(
            [0],
            [0],
            marker="o",
            mfc=all_colors[0],
            mec="black",
            label="CARP",
            markersize=12,
            linestyle="None",
        )
    )

    return legend_items

def plot_latvssel_inner(ax: plt.Axes, all_colors: list[str]):
    basedir = c.get_plotdata_dir()
    csv_path = basedir / "querylog.csv"
    df_carp, df_flat, df_fq, df_scan = read_query_csvs(csv_path)

    x = df_carp["timemean"]
    y = df_fq["timemean"]
    y/x

    markers = ["o", "D", "^", "s"]
    all_labels = ["DeltaFS/FullScan", "FastQuery", "TritonSort", "CARP"]
    all_msz = [16, 14, 14, 14]

    for type, df in enumerate([df_carp, df_flat, df_fq, df_scan]):
        rowidx = 0
        for index, row in df.iterrows():
            data_x = row["qsel"]
            if type < 3:
                data_y = row["timemean"]
                data_err = row["timestd"]
            else:
                data_y = row["time"]

            marker = markers[type]
            color = all_colors[type]

            if type == 0:
                zorder = 3
            else:
                zorder = 2
            ax.plot(
                data_x,
                data_y,
                marker=marker,
                mec="black",
                mfc=color,
                markersize=all_msz[type],
                label=all_labels[type],
                zorder=zorder,
            )
            if type < 3:
                ax.errorbar(data_x, data_y, yerr=data_err, color=color, capsize=3, zorder=1)

            rowidx += 1

    ax.legend(
        handles=get_legend_items(all_colors),
        handletextpad=0.2,
        borderpad=0.2,
        columnspacing=0.6,
        fontsize=18,
        loc="lower left",
        bbox_to_anchor=(0.18, 0.02),
        ncol=2,
    )

    ax.set_yscale("log")
    yticks = [0.04, 0.2, 1, 5, 25, 125]
    yticks = [0.017, 0.07, 0.3, 1.25, 5, 20, 80, 320]
    yticks = [0.01, 0.1, 1, 10, 100, 330]
    # yticks = [0.04, 0.2, 1, 5, 20, 80, 320]
    ax.set_yticks(yticks)

    def tickfmt(x):
        if x - int(x) < 0.01:
            return "{:d}".format(x)
        else:
            return "{:.2f}".format(x)

    ax.set_yticklabels([tickfmt(y) for y in yticks])

    def latfmt(x, pos):
        if x < 1:
            return "{:.2f}\\,s".format(x)
        else:
            return "{:.0f}\\,s".format(x)

    ax.yaxis.set_major_formatter(FuncFormatter(latfmt))

    ax.set_xlabel(r"\textbf{Query Selectivity}")
    ax.set_ylabel(r"\textbf{Query Latency}")

    # ax.minorticks_off()
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    ax.xaxis.set_major_formatter("{x:.1f}\%")

    # for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    #     label.set_fontsize(base_fontsz - 1)

    ax.xaxis.grid(True, color="#777", which="major")
    ax.xaxis.grid(True, color="#ddd", which="minor")
    # ax.yaxis.grid(True, color='#bbb', which='major')
    ax.yaxis.grid(True, color="#777", which="major")
    ax.yaxis.grid(True, color="#ddd", which="minor")


def plot_query_latvssel_unified():
    cmap = plt.colormaps["Pastel1"]
    # all_cidxs = [0, 5, 2, 3]
    # all_colors = [cmap(i) for i in all_cidxs]
    all_colors = [cmap(i) for i in range(4)]

    fig, ax = plt.subplots(1, 1, figsize=[7, 6])
    fig.clear()
    ax = fig.add_subplot(111)
    plot_latvssel_inner(ax, all_colors)
    fig.tight_layout()

    alx_carp = (list(range(0, 40)), [], [])
    alx_ts = (list(range(40, 80)), [], [])
    alx_fq = (list(range(80, 120)), [], [])
    alx_dfs = (list(range(120, 128)), [], [])
    all_alx = [alx_carp, alx_ts, alx_fq, alx_dfs]

    sb = c.StagedBuildout(ax, fig, "qlatvssel")
    sb.disable_alx(*alx_carp)
    sb.disable_alx(*alx_ts)
    sb.disable_alx(*alx_fq)
    sb.disable_alx(*alx_dfs)

    sb.enable_alx(*alx_dfs)
    c.save_plot(fig, "qlatvssel.f1")

    sb.enable_alx(*alx_ts)
    c.save_plot(fig, "qlatvssel.f2")

    sb.enable_alx(*alx_fq)
    c.save_plot(fig, "qlatvssel.f3")

    sb.enable_alx(*alx_carp)
    c.save_plot(fig, "qlatvssel.f4")

    plt.close(fig)


def run():
    plot_query_latvssel_unified()


if __name__ == "__main__":
    plt.style.use(c.get_plotsrc_dir() / "ppt.mplstyle")
    run()
