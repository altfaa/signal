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
    ax.set_title(f'Лидеры тороговли MOEX {tittle}, %', fontsize=16)
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

    y1 = 0.133
    y2 = y1 - 0.04
    y3 = y2 - 0.03

    x1 = 0.23
    x2 = x1 + 0.2
    x3 = x2 + 0.2

    ax.text(x1, y1, f"{name1}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(x1, y2, f"{vol1/ 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(x1, y3, f"{cost1 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)

    ax.text(x2, y1, f"{name2}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(x2, y2, f"{vol2 / 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(x2, y3, f"{cost2 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)

    ax.text(x3, y1, f"{name3}", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=16)
    ax.text(x3, y2, f"{vol3 / 1000000:.1f} млн.лотов.", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)
    ax.text(x3, y3, f"{cost3 / 1000000000:.1f} млрд. ₽", horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes, fontsize=14)



    ax.text(0.87, 0.03, "@moex signal", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
            fontsize=14)

    plt.show()
    plt.savefig(out_filename, dpi=200, bbox_inches='tight')
    plt.close(fig)
