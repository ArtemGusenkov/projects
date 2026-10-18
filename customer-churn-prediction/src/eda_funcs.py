import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def plot_bin_bars(df, y, bar_col, title, xlabel, xticks_1, xticks_2, x1_rot=0):
    df[bar_col] = df[bar_col].replace({'Y':1, 'N':-1})
    df[bar_col] = df[bar_col].fillna(0)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
    bar1 = df[bar_col].value_counts(normalize=True)
    sns.barplot(bar1, ax=ax[0])
    ax[0].set_xticks(ticks=[0, 1, 2], labels=xticks_1, rotation=x1_rot)
    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel('доля клиентов')
    ax[0].set_title(title)

    temp_df = pd.concat((df[bar_col],y),axis=1)
    temp_df = temp_df.groupby(bar_col).mean()
    ax[1].bar(temp_df.index, temp_df.values[:, 0], alpha=0.8, label='ушедшие клиенты', color='#db5649')
    ax[1].axhline(y.mean(), color='gray', linestyle='--', label='общий процент отток клиентов')
    ax[1].set_xticks(ticks=[-1, 0, 1], labels=xticks_2)
    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel('доля уходящих клиентов')
    ax[1].legend()
    ax[1].set_title('доля ушедших клиентов \n внутри каждой категории')

    plt.tight_layout()
    plt.show()


def trip_plot(df, y, col_name, title2, xlabel):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(14, 5))

    count_na = df[col_name].isna().sum()
    count_ntna = df[col_name].notna().sum()
    ax[0].pie([count_na, count_ntna], labels=('нет данных', ' есть \n информация'),
            autopct='%1.1f%%')
    ax[0].set_title('доли клиентов с метками и без')

    bar1 = df[col_name].value_counts(normalize=True, dropna=False)
    sns.barplot(bar1, ax=ax[1])
    ax[1].set_title(title2)
    ax[1].set_xlabel(xlabel)

    temp_df = pd.concat((df[col_name],y),axis=1)
    temp_df = temp_df.groupby(col_name).mean()
    ax[2].bar(temp_df.index, temp_df.values[:, 0], alpha=0.8, label='ушедшие клиенты', color='#db5649')
    ax[2].axhline(y.mean(), color='gray', linestyle='--', label='общий процент отток клиентов')
    ax[2].set_title('доля ушедших клиентов \n внутри каждой категории')
    ax[2].set_xlabel(xlabel)

    plt.tight_layout()
    plt.show()  


def plot_2_barplots(df, y, bar_col, title, xlabel):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    bar1 = df[bar_col].value_counts(normalize=True)
    sns.barplot(bar1, ax=ax[0])
    ax[0].set_xticks(ticks=range(len(bar1.index)), labels=bar1.index, rotation=70)
    ax[0].set_xlabel(xlabel)
    ax[0].set_title(title)

    temp_df = pd.concat((df[bar_col],y),axis=1)
    temp_df = temp_df.groupby(bar_col).mean()
    temp_df = temp_df.reindex(bar1.index)
    ax[1].bar(temp_df.index, temp_df.values[:, 0], alpha=0.8, label='доли ушедших клиентов', color='#db5649')
    ax[1].axhline(y.mean(), color='gray', linestyle='--', label='общий процент отток клиентов')
    ax[1].set_xticks(ticks=range(len(temp_df.index)), labels=temp_df.index, rotation=70)
    ax[1].set_xlabel(xlabel)
    ax[1].legend()
    ax[1].set_title('доля ушедших клиентов \n внутри каждой категории')

    plt.tight_layout()
    plt.show()


def reg_plot(df, y, col_name, title, xlabel):
    y = y.replace({0:'оставшиеся клиенты', 1:'ушедшие клиенты'})
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

    count_na = df[col_name].isna().sum()
    count_ntna = df[col_name].notna().sum()
    ax[0].pie([count_na, count_ntna], labels=('нет данных', ' есть \n информация'), autopct='%1.1f%%')
    ax[0].set_title('доли клиентов с метками и без')

    bar1 = df[col_name].value_counts(normalize=True)
    bar2 = bar1[bar1>0.002]
    bar2.loc['other'] = bar1[bar1<=0.001].sum()
    sns.barplot(bar2, ax=ax[1])
    ax[1].set_title(title)
    ax[1].set_xticks(ticks=range(len(bar2.index)), labels=bar2.index, rotation=90)
    ax[1].set_xlabel(xlabel)

    plt.tight_layout()
    plt.show()  


def plot_2_hists(df, y, bar_col, title, xlabel, log:False):
    y = y.replace({0:'оставшиеся клиенты', 1:'ушедшие клиенты'})
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    if log==False:
        sns.histplot(df[bar_col], ax=ax[0])
    else:
        sns.histplot(df[bar_col], ax=ax[0], log_scale=log)
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel)

    plot_data = df[bar_col][df[bar_col]>0]
    if log==False:
        sns.histplot(x=plot_data, hue=y, ax=ax[1], stat='percent', common_norm=None)
    else:
        sns.histplot(x=plot_data, hue=y, ax=ax[1], stat='percent', common_norm=None, log_scale=log)
    ax[1].set_title('сравнение долей ушедших и оставшихся клиентов')
    ax[1].set_xlabel(xlabel)

    plt.tight_layout()
    plt.show()


def nums_hists(df, y, bar_col_start_with, glob_title):
    prod_cnt_cols = [i for i in df.columns if i.startswith(bar_col_start_with)]
    fig = plt.figure(figsize=(14,9))
    for en, i in enumerate(prod_cnt_cols):
        ax = fig.add_subplot(3, 4, en+1)
        if (df[i] == 0).sum() / df[i].count() > 0.8:
            mask = df[i] != 0
            sns.histplot(x=df.loc[mask, i], hue=y[mask], stat='percent', common_norm=False, bins=20, alpha=0.5, ax=ax)
        else:
            sns.histplot(x=df[i], hue=y, stat='percent', common_norm=False, bins=20, alpha=0.5, ax=ax)
        ax.set_title(i)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.suptitle(glob_title, fontsize=16)
    plt.show()