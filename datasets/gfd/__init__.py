import os
import pandas as pd
import tqdm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


__name__ = 'gfd'


def load_data(label='h', load=0):
    assert label in ['h', 'b']
    assert load in [i for i in range(0, 100, 10)]
    return pd.read_csv(os.path.dirname(__file__) + f'/{label}30hz{load}.csv.gz')


def plot_sequence(df, st=0, ed=None, ax=None, figsize=(10, 3), individual=True):

    if ed is None:
        ed = df.shape[0]

    if individual:
        if not ax is None:
            assert len(ax) == 4
        else:
            fig, ax = plt.subplots(4, figsize=figsize)

        for i in range(4):
            df.iloc[st:ed, i].plot(ax=ax[i], figsize=figsize, legend=True)

    else:
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        df.iloc[st:ed].plot(ax=ax, figsize=figsize, legend=True)


def gen_summary(outdir=None, st=0, ed=500, wd=20, hg=8):

    if outdir is None:
        outdir = os.path.dirname(__file__)

    os.makedirs(outdir, exist_ok=True)

    with PdfPages(outdir + '/gfd_summary.pdf') as pp:
        for label in ['h', 'b']:
            for load in tqdm.trange(0, 100, 10, desc=label):
                fig, ax = plt.subplots(5)

                plot_sequence(load_data(label=label, load=load), st=st, ed=ed, ax=ax[:4], figsize=(wd, hg), individual=True)
                plot_sequence(load_data(label=label, load=load), st=st, ed=ed, ax=ax[-1], figsize=(wd, hg), individual=False)

                ax[-1].set_xlabel('Time')
                for axi in ax: axi.set_ylabel('Value')
                name = 'Healty' if label == 'h' else 'BrokenTooth'
                ax[0].set_title(f'{name}: Load= {load}')

                fig.savefig(pp, bbox_inches='tight', format='pdf')
                plt.clf()
                plt.close()