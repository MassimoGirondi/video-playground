import pandas as pd
import matplotlib.pyplot as plt
import argparse
from plotter import *
from glob import  glob
import re



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=".")

    args = parser.parse_args()


    data = []
    for f in glob(f"{args.input}/*/output.csv"):
        print(f)
        df = read_file(f)
        model = re.match(r"(?P<path>.*)/(?P<model>.*)/(?P<file>.*).csv", f).groupdict()["model"]
        df["model"] = model

        data += [df]

    data = pd.concat(data)

    data_times = []

    for f in glob(f"{args.input}/*/output-times.csv"):
        print(f)
        df = read_file(f)
        model = re.match(r"(?P<path>.*)/(?P<model>.*)/(?P<file>.*).csv", f).groupdict()["model"]
        df["model"] = model
        data_times += [df]

    data_times = pd.concat(data_times)

    if "sm_usage" in data_times.columns and "mem_usage" in data_times.columns:
        print(data_times)
        #s = sns.lineplot(data=data_times, x=data_times.index, y="sm_usage", hue="model")

        fig, ax = plt.subplots()
        for gname, gdata in data_times.groupby("model"):
            ax.plot(gdata["sm_usage"], label =gname)

        ax.legend()
        fig.savefig(f"{args.input}/sm_usage.pdf")
        del data_times["sm_usage"]
        del data_times["mem_usage"]


    s = sns.catplot(data=data, x="model", y="fps", kind="violin", errorbar="pi", bw_adjust=10,)
    plt.ylim(0,29)
    s.savefig(f"{args.input}/fps-violins.pdf")

    s = sns.catplot(data=data, x="model", y="t", kind="violin", errorbar="pi", bw_adjust=10,)
    plt.ylim(0,.3)
    s.savefig(f"{args.input}/t-violins.pdf")


    fig, ax = plt.subplots()
    #s = sns.barplot(data=data, x="model")
    avg = data_times.groupby("model").mean()
    low = data_times.groupby("model").quantile(.25)
    high = data_times.groupby("model").quantile(.75)
    avg.plot(kind="bar", stacked=True) #, yerr=[h-l for h,l in zip(high, low)] )

    # print(avg)
    # data_times.plot(kind="bar", stacked=True)
    plt.savefig(f"{args.input}/time-components.pdf")


    # fig = violinplot(data, y="t", bw)
    # fig.savefig(f"{args.input}/latency-violins.pdf")
    # fig = violinplot(data)
    # fig.savefig(f"{args.input}/fps-violins.pdf")



    # fig = plot_components_time(df_times)

    # fig = plot_fps_dist(df)
    # fig.savefig(f"{args.output}-fps.pdf")

    # fig = plot_latency_dist(df)
    # fig.savefig(f"{args.output}-latency.pdf")



