import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_bin_bars(df, y, bar_col, title, xlabel, xticks_1, xticks_2, x1_rot=0):
    df[bar_col] = df[bar_col].replace({'Y':1, 'N':-1})
    df[bar_col] = df[bar_col].fillna(0)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
    bar1 = df[bar_col].value_counts(normalize=True)
    sns.barplot(bar1, ax=ax[0])
    ax[0].set_xticks(ticks=[0, 1, 2], labels=xticks_1, rotation=x1_rot)
    ax[0].set_xlabel(xlabel)
    ax[0].set_title(title)

    bar1 = df[bar_col][(df[bar_col] != 0) & (y==0)].value_counts(normalize=True)
    bar2 = df[bar_col][(df[bar_col] != 0) & (y==1)].value_counts(normalize=True)
    ax[1].bar(bar1.index - 0.3, bar1.values, alpha=0.5, label='оставшиеся клиенты')
    ax[1].bar(bar2.index, bar2.values, alpha=0.5, label='ушедшие клиенты', color='#db5649')
    ax[1].set_xticks(ticks=[-1, 1], labels=xticks_2)
    ax[1].set_xlabel(xlabel)
    ax[1].legend()
    ax[1].set_title('сравнение ушедших и оставшихся клиентов')

    plt.tight_layout()
    plt.show()


def plot_2_barplots(df, y, bar_col, title, xlabel):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    bar1 = df[bar_col].value_counts(normalize=True)
    sns.barplot(bar1, ax=ax[0])
    ax[0].set_xticks(ticks=range(len(bar1.index)), labels=bar1.index, rotation=70)
    ax[0].set_xlabel(xlabel)
    ax[0].set_title(title)

    plot_data = pd.concat((df[bar_col], y, 1-y), axis=1, keys=[bar_col, 'TARG_1', 'TARG_0'])
    plot_data = plot_data.groupby(by=[bar_col], sort=False).sum()/plot_data.groupby(by=[bar_col]).sum().sum()
    plot_data = plot_data.reindex(bar1.index)
    x = np.arange(len(plot_data))
    width = 0.4
    ax[1].bar(x=(x-(width/2)), height=plot_data['TARG_1'], width=width, label='ушедшие клиенты', color='#db5649')
    ax[1].bar(x=(x+(width/2)), height=plot_data['TARG_0'], width=width, label='оставшиеся клиенты', alpha=0.5)
    ax[1].set_xticks(ticks=range(len(bar1.index)), labels=plot_data.index, rotation=70)
    ax[1].set_xlabel(xlabel)
    ax[1].legend()
    ax[1].set_title('сравнение долей ушедших \n и оставшихся клиентов')

    plt.tight_layout()
    plt.show()


def plot_2_hists(df, y, bar_col, title, xlabel, log:False):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    if log==False:
        sns.histplot(df[bar_col], ax=ax[0])
    else:
        sns.histplot(np.log10(df[bar_col]), ax=ax[0])
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel)

    plot_data = df[bar_col][df[bar_col]>0]
    if log==False:
        plot_data = plot_data
    else:
        plot_data = np.log10(plot_data)
    sns.histplot(x=plot_data, hue=y, ax=ax[1], stat='percent', common_norm=None)
    ax[1].set_title('сравнение долей ушедших и оставшихся клиентов')
    ax[1].set_xlabel(xlabel)

    plt.tight_layout()
    plt.show()