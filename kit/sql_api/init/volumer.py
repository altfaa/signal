from kit.catalog.get_full_moex_dicts import ticker_to_figi
from datetime import datetime, timedelta
from os import system
from kit.pathes.quotes import DB_NAME_QUOTES_5M
from kit.pathes.volume import DB_NAME_VOLUMER
import sqlite3 as sl
import pandas as pd
from kit.catalog.get_lots_info import ticker_to_lots


def get_day_volume_from_db(ticker, date):
    user_year = date.year
    user_month = date.month
    user_day = date.day

    d1 = datetime(year=user_year, month=user_month, day=user_day, hour=9, minute=59).strftime("%Y-%m-%d %H:%M")
    d2 = datetime(year=user_year, month=user_month, day=user_day, hour=23, minute=59).strftime("%Y-%m-%d %H:%M")

    con = sl.connect(DB_NAME_QUOTES_5M)
    with con:
        command = f"SELECT * FROM {ticker} WHERE DATE > '{d1}' AND DATE < '{d2}'"

        df = pd.read_sql(command, con)
        df.Open = df.Open.astype(float)
        df.Close = df.Close.astype(float)
        df.Low = df.Low.astype(float)
        df.High = df.High.astype(float)
        df.Volume = df.Volume.astype(int)
        return df.Volume.sum(), (df.Volume * df.Close * int(ticker_to_lots[ticker])).sum()


def put_total_day_volume(ticker, date):
    volume, cost = get_day_volume_from_db(ticker, date)
    # dict = {date.strftime("%Y-%m-%d"): volume, }
    print([date.strftime("%Y-%m-%d"), volume, cost])
    df = pd.DataFrame([[date.strftime("%Y-%m-%d"), volume, cost]], columns=['Day', 'Volume', 'Cost'])
    print(df)
    con = sl.connect(DB_NAME_VOLUMER)
    if volume:
        with con:
            inserted_count = df.to_sql(name=ticker, con=con, if_exists='append',
                                       index=False)
            con.commit()


def init_volume():
    for ticker in ticker_to_figi:
        # start_date = datetime.strptime(d, "%Y-%m-%d %H:%M")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        res = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        )
        for date in res:
            put_total_day_volume(ticker, date)


def init_volume_with_system_commands():
    buffer_mark = "_buffer"
    delete_command = f"rm {DB_NAME_VOLUMER}"
    delete_buf_command = f"rm {DB_NAME_VOLUMER}{buffer_mark}"
    move_command = f"mv {DB_NAME_VOLUMER}{buffer_mark} {DB_NAME_VOLUMER}"
    system(delete_buf_command)
    if init_volume():
        system(delete_command)
        system(move_command)
