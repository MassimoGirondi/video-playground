import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import seaborn as sns

def read_file(file):
    df = pd.read_csv(file, index_col=0)
    return df



def plot_components_time(df):
    fig, ax = plt.subplots()
    # Can we avoid the list generator here?
    ax.stackplot(df.index, *[df[col] for col in df.columns], labels=df.columns)
    ax.set_xlabel("Timestamp (s)")
    ax.set_ylabel("Comulative time (us)")
    ax.legend()
    return fig

def cut_plot_dist(ax, values, low=.1, high=.9):
    print(values.quantile(low), values.quantile(high))
    if low != 0:
        ax.set_xlim(values.quantile(low), values.quantile(high))
    else:
        ax.set_xlim(0,values.quantile(high))



def plot_fps_dist(df):
    fig, ax = plt.subplots()
    ax.hist(df.fps, bins=50,density=True, label="FPS measured")
    kde_xs = np.linspace(1, 30, 100)
    kde = st.gaussian_kde(df.fps)
    ax.plot(kde_xs, kde.pdf(kde_xs), label="PDF")
    ax.set_xlabel("Frames per second")
    ax.set_ylabel("Probability")
    cut_plot_dist(ax, df.fps, low=0.001, high=.99999)
    ax.legend()
    return fig


def plot_latency_dist(df):
    fig, ax = plt.subplots()
    ax.hist(df.t, bins=100,density=True, label="Latency measured")
    kde_xs = np.linspace(.002, .3, 1000)
    kde = st.gaussian_kde(df.t)
    ax.plot(kde_xs, kde.pdf(kde_xs), label="PDF")
    cut_plot_dist(ax, df.t, low=0.00001, high=.995)
    ax.set_xlabel("Frame latency (s)")
    ax.set_ylabel("Probability")
    ax.legend()
    return fig

def violinplot(data, y="fps"):
    s = sns.catplot(data=data, x="model", y=y, kind="violin", errorbar="pi", bw_adjust=20,)
    #s = sns.swarmplot(data=data, x="model", y="fps", size=3)
    return s._figure
