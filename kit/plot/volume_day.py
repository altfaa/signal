import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas
import pandas as pd
import datetime
import numpy as np
import locale

locale.setlocale(locale.LC_ALL, "")


def good_make_table_volumes(df, out_filename, tittle, info):
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

    name1 = info[0][0]
    name2 = info[0][1]
    name3 = info[0][2]

    vol1 = info[1][0]
    vol2 = info[1][1]
    vol3 = info[1][2]

    cost1 = info[2][0]
    cost2 = info[2][1]
    cost3 = info[2][2]

    y1 = 0.11
    y2 = 0.07
    y3 = 0.04

    ax.text(0.2, y1, f"{name1}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(0.2, y2, f"{vol1/ 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(0.2, y3, f"{cost1 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)

    ax.text(0.4, y1, f"{name2}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(0.4, y2, f"{vol2 / 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(0.4, y3, f"{cost2 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)

    ax.text(0.6, y1, f"{name3}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(0.6, y2, f"{vol3 / 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(0.6, y3, f"{cost3 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)



    ax.text(0.87, 0.03, "@moex signal", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=14)

    plt.show()
    plt.savefig(out_filename, dpi=200, bbox_inches='tight')
    plt.close(fig)
