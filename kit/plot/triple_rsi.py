from kit.names.channel import CHANNEL_NAME

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import ta.momentum
import ta.trend


def f_color(x):
    if x >= 0:
        return '#96D7A1'
    else:
        return '#FCADB8'


def draw_rsi_3_plot(df, ticker, out_filename, delta_days: int):
    rsi_window = 14
    mpl.use('agg')
    last_price = df['Close'].iloc[-1]
    date_axes_count = 5
    text = f"{ticker} {delta_days}"
    fig, (ax2, ax1, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    fig.subplots_adjust(hspace=0)
    plt.xticks(rotation=0)
    plt.xticks(np.arange(0, df['Date'].count(), df['Date'].count() / date_axes_count - 1))

    last_num = df['Open'].count()
    hlines_value = df['Open'].min()
    count = 0
    while hlines_value < df['Open'].max():
        ax1.hlines(hlines_value, 0, last_num, linewidth=0.1, color='green', linestyles=':')
        hlines_value += hlines_value * 0.01
        count += 1

    ax1.plot(df['Date'], df['Close'], label=f'price Δ{count}% ', linewidth=0.99, color='#3CAEFA')
    ax1twinx = ax1.twinx()
    ax1twinx.bar(df['Date'], df['Volume'].apply(lambda x: x / 1000), label='volume', linewidth=0.4, color='blue',
                 alpha=0.25)

    rsi_series = ta.momentum.rsi(close=df['Close'], window=rsi_window, fillna=False)
    ax2.plot(df['Date'], rsi_series, label=f'rsi-{rsi_window}', linewidth=0.5, color='#1BB984')

    ax2.hlines(15, 0, df['Date'].count(), linewidth=0.3, color='red')
    ax2.hlines(20, 0, df['Date'].count(), linewidth=0.2, color='red')
    ax2.hlines(25, 0, df['Date'].count(), linewidth=0.1, color='red')
    ax2.hlines(30, 0, df['Date'].count(), linewidth=0.05, color='red')
    ax2.hlines(70, 0, df['Date'].count(), linewidth=0.05, color='blue')
    ax2.hlines(75, 0, df['Date'].count(), linewidth=0.1, color='blue')
    ax2.hlines(80, 0, df['Date'].count(), linewidth=0.2, color='blue')
    ax2.hlines(85, 0, df['Date'].count(), linewidth=0.3, color='blue')

    tsi_ser = ta.momentum.tsi(close=df.Close, window_fast=13, window_slow=25, fillna=False)
    ema_ser = ta.trend.ema_indicator(close=tsi_ser, window=13, fillna=False)
    dif_tsi_ema_ser = tsi_ser - ema_ser
    tsi_bar_color_ser = dif_tsi_ema_ser.apply(f_color)

    ax3.plot(df['Date'], tsi_ser, label=f'tsi-25-13', linewidth=0.3, color='red')
    ax3.plot(df['Date'], ema_ser, label=f'ema-13', linewidth=0.3, color='blue')

    ax3.bar(df['Date'], dif_tsi_ema_ser, color=tsi_bar_color_ser)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left')
    ax3.legend(loc='upper left')
    ax1twinx.legend(loc='lower left')

    ax2.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    ax3.text(0.01, 0.1, text, horizontalalignment='left', verticalalignment='center', transform=ax3.transAxes,
             fontsize=16)
    ax3.text(0.01, 0.2, f"Close price: {last_price}", horizontalalignment='left', verticalalignment='center',
             transform=ax3.transAxes)
    ax3.text(0.83, 0.1, CHANNEL_NAME, horizontalalignment='left', verticalalignment='center', transform=ax3.transAxes)

    plt.savefig(out_filename)
    plt.close(fig)

    return 1
