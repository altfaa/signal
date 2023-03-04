import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas
import pandas as pd
import datetime
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, "")


def good_make_table_volumes(df, out_filename, tittle):
    df = df.head(20)
    mpl.use('agg')  # отключение визуальной части

    fig, ax = plt.subplots(figsize=(15, 10))
    tickers = df.Name
    y_pos = np.arange(len(tickers))
    ax.barh(y_pos, df['%'], align='center', height=0.7)
    ax.set_yticks(y_pos, labels=tickers)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Процент сделок')
    ax.set_title(f'Объемы торговли акциями MOEX {tittle}, %')
    ax.bar_label(ax.containers[0])
    ax.axes.get_xaxis().set_visible(False)
    plt.show()
    plt.savefig(out_filename, dpi=200, bbox_inches='tight')
    plt.close(fig)