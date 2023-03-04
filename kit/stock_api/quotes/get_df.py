__all__ = ['get_df_from_stock']

from kit.tokens.tinkoff import token
from tinkoff.invest import Client, CandleInterval
import pandas as pd
import datetime


def get_and_check_date():
    holidays_str = ["2023-03-08", "2023-05-01", "2023-05-09"]
    ### TO DO ###
    holidays_datetime = []
    date_now = datetime.datetime.now()

    if date_now.hour < 10:
        return False
    else:
        return date_now


def get_df_from_candles(candles):
    list_open, list_close, list_high, list_low, list_vol, list_time = [], [], [], [], [], []

    for frame in candles.candles:
        beauty_time = (frame.time + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
        cur_open = frame.open.units + frame.open.nano / 1000000000
        cur_close = frame.close.units + frame.close.nano / 1000000000
        cur_high = frame.high.units + frame.high.nano / 1000000000
        cur_low = frame.low.units + frame.low.nano / 1000000000
        cur_volume = frame.volume

        list_open.append(cur_open)
        list_high.append(cur_high)
        list_low.append(cur_low)
        list_close.append(cur_close)
        list_vol.append(cur_volume)
        list_time.append(beauty_time)
    df = pd.DataFrame({
        'Open': list_open,
        'High': list_high,
        'Low': list_low,
        'Close': list_close,
        'Volume': list_vol,
        'Date': list_time
    })
    return df


def get_df_from_stock(figi, interval, date_start: datetime, date_end: datetime):
    __doc__ = "interval is 5m or 15m"
    if interval == "5m":
        candle_interval = CandleInterval.CANDLE_INTERVAL_5_MIN
    elif interval == "15m":
        candle_interval = CandleInterval.CANDLE_INTERVAL_15_MIN
    else:
        return False

    with Client(token) as client:
        candles = client.market_data.get_candles(
            figi=figi,
            from_=date_start,
            to=date_end,
            interval=candle_interval
        )
    return get_df_from_candles(candles)


def get_empty_df_quotes():
    return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Date'])


def get_df_from_stock_many_days(date1, date2, figi, interval):
    user_year = date1.year
    user_month = date1.month
    user_day = date1.day
    start_date = datetime.datetime(year=user_year, month=user_month, day=user_day, hour=10)
    delta = date2 - date1
    days_num = delta.days
    df = get_empty_df_quotes()
    for one_day in (range(0, days_num + 1)):
        cur_date1 = start_date + datetime.timedelta(days=one_day)
        if cur_date1.weekday() in [5, 6]:  ## выходные пропускаем (субботу вскресенье)
            continue
        cur_date2 = cur_date1 + datetime.timedelta(hours=13)
        df_step = get_df_from_stock(figi=figi, date_start=cur_date1, date_end=cur_date2, interval=interval)
        df = pd.concat(df, df_step, ignore_index=True)

    return df
