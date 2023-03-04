import sqlite3 as sl
import pandas as pd


def get_df_from_quotes_after_date(ticker, date_start, db_path):
    con = sl.connect(db_path)
    with con:
        command = f"SELECT * FROM {ticker} WHERE DATE > '{date_start}'"
        df = pd.read_sql(command, con)

        df.Open = df.Open.astype(float)
        df.Close = df.Close.astype(float)
        df.Low = df.Low.astype(float)
        df.High = df.High.astype(float)
        df.Volume = df.Volume.astype(int)
        return df


def get_df_volume_from_db(ticker, date_start, db_path):
    con = sl.connect(db_path)
    with con:
        command = f"SELECT * FROM {ticker} WHERE DAY > '{date_start}'"
        df = pd.read_sql(command, con)
        df.Day = df.Day
        df.Volume = df.Volume.astype(int)
        return df


def get_df_all_volumes(date, db_path, ticker_to_figi):
    print(date)
    # df = pd.DataFrame()
    last_date = str(date)[0:10]
    con = sl.connect(db_path)
    cursor = con.cursor()
    list_ticker = []
    list_vol = []
    list_proc = []
    with con:
        for ticker in ticker_to_figi:
            cursor.execute(f"SELECT Day, Volume FROM {ticker} WHERE Day ='{last_date}'")
            data = cursor.fetchall()
            for row in data:
                list_vol.append(row[1])
                list_ticker.append(ticker)
    total = sum(list_vol)

    name_s = pd.Series(list_ticker)
    vol_s = pd.Series(list_vol)
    # price_s = pd.Series(list_price)
    # sum_s = pd.Series(list_sum)
    # proc_s = pd.Series(list_procent)

    name_df = name_s.to_frame(name='Name')
    vol_df = vol_s.to_frame(name='Volumes')
    # price_df = price_s.to_frame(name='Price')
    # sum_df = sum_s.to_frame(name='Sum')
    # procent_df = proc_s.to_frame(name='%')
    #
    df = pd.concat([name_df, vol_df], axis=1)

    df['Name'] = name_s
    df['Volumes'] = vol_s
    df['%'] = df['Volumes'] / total * 100

    df = df.round({'%': 2})

    return df.sort_values('%', ascending=False)
