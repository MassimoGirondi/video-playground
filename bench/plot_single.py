import pandas as pd
import matplotlib.pyplot as plt
import argparse
from plotter import *



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="output.csv")
    parser.add_argument("--input-times", type=str, default="output-times.csv")
    parser.add_argument("--output", type=str, default="plot")

    args = parser.parse_args()
    df = read_file(args.input)
    df_times = read_file(args.input_times)


    fig = plot_components_time(df_times)
    fig.savefig(f"{args.output}-times.pdf")

    fig = plot_fps_dist(df)
    fig.savefig(f"{args.output}-fps.pdf")

    fig = plot_latency_dist(df)
    fig.savefig(f"{args.output}-latency.pdf")



