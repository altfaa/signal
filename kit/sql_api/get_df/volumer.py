import pandas as pd
import sqlite3 as sl
from kit.pathes.volume import DB_NAME_VOLUMER
from kit.catalog.get_full_moex_dicts import ticker_to_figi


def get_df_all_volumes(date):
    print(date)
    # df = pd.DataFrame()
    last_date = str(date)[0:10]
    con = sl.connect(DB_NAME_VOLUMER)
    cursor = con.cursor()
    list_ticker = []
    list_vol = []
    list_cost = []
    with con:
        for ticker in ticker_to_figi:
            try:
                cursor.execute(f"SELECT Day, Volume, Cost FROM {ticker} WHERE Day ='{last_date}'")
                data = cursor.fetchall()
                for row in data:
                    list_vol.append(row[1])
                    list_cost.append(row[2])
                    list_ticker.append(ticker)
            except Exception as e:
                print(e)
    total = sum(list_cost)

    name_s = pd.Series(list_ticker)
    cost_s = pd.Series(list_cost)
    vol_s = pd.Series(list_vol)

    name_df = name_s.to_frame(name='Name')
    vol_df = cost_s.to_frame(name='Volumes')

    df = pd.concat([name_df, vol_df], axis=1)

    df['Name'] = name_s
    df['Volumes'] = vol_s
    df['Cost'] = cost_s
    df['%'] = df['Cost'] / total * 100

    df = df.round({'%': 2})

    df_out = df.sort_values('%', ascending=False)

    name = df_out.Name.iloc[0]
    vol = df_out.Volumes.iloc[0]
    cost = df_out.Cost.iloc[0]
    info_list = [name, vol, cost, total]

    return df_out, info_list
