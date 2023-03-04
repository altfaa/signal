from kit.catalog.get_full_moex_dicts import ticker_to_figi, ticker_to_name
from kit.sql_api.get_df.quotes import get_df_from_quotes_after_date
from kit.pathes.quotes import DB_NAME_QUOTES_5M
from kit.plot.triple_rsi import draw_rsi_3_plot
from kit.names.channel import CHANNEL_NAME
from kit.telegram_api.send import send_photo_to_my_channel
from ta import momentum
from datetime import datetime, timedelta
from locale import setlocale, LC_ALL

setlocale(LC_ALL, "")

low = 20
heigh = 73

for ticker in ticker_to_figi:
    df = get_df_from_quotes_after_date(ticker=ticker, date_start=datetime.now() - timedelta(days=7),
                                       db_path=DB_NAME_QUOTES_5M)

    if(df.empty):
        continue
    rsi_window = 14
    rsi_series = momentum.rsi(close=df['Close'], window=rsi_window, fillna=False)
    r, c = df.shape
    last_date = df['Date'].iloc[-1]
    last_date_datetype = datetime.strptime(last_date, '%Y-%m-%d %H:%M')

    now_date = datetime.now()
    time_delta = now_date - last_date_datetype


    if time_delta > timedelta(hours=25):
        print(f"{ticker} timedelta > 10 min")
        continue

    last_rsi = rsi_series[r - 1]
    prev_rsi_1 = rsi_series[r - 2]
    prev_rsi_2 = rsi_series[r - 3]
    prev_rsi_3 = rsi_series[r - 4]
    prev_rsi_4 = rsi_series[r - 5]
    out_filename = "rsi_checker_5.png"
    if last_rsi > heigh or last_rsi < low:
        if (last_rsi > heigh and last_rsi > prev_rsi_1 and last_rsi > prev_rsi_2 and last_rsi > prev_rsi_3 and last_rsi > prev_rsi_4) or (
                last_rsi < low and last_rsi < prev_rsi_1 and last_rsi < prev_rsi_2 and last_rsi < prev_rsi_3 and last_rsi < prev_rsi_4):
            last_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]

            procent_change = (last_price - prev_price) * 100 / prev_price
            text_price = "{:1.2f}".format(last_price)
            text_procent = "{:15.2f}".format(procent_change)
            text_last_rsi = "{:1.2f}".format(last_rsi)
            text_volume = "{:15.0f}".format(df['Volume'].iloc[-1])

            name = ticker_to_name[ticker]

            text_last_date = last_date_datetype.strftime("%d %b %Y %H:%M")

            text_message = f"#{ticker} {name}\n\n⏰ *RSI Сигнал*\n\n🗓 {text_last_date}\n\n    _Price:_ {text_price} ₽\n    _RSI-14:_ {text_last_rsi}\n\n" + f"{CHANNEL_NAME}".replace("_","\\_")
            print(text_message)
            draw_rsi_3_plot(df=df, ticker=ticker, out_filename=out_filename, delta_days=7)
            photo_fp = open(out_filename, 'rb')
            send_photo_to_my_channel(photo_fp=photo_fp, text_message=text_message)
            photo_fp.close()
