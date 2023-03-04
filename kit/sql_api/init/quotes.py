from ..common import create_ticker_table_in_quotes, put_df_to_db
from kit.catalog.get_full_moex_dicts import ticker_to_figi
from kit.stock_api.quotes.get_df import get_df_from_stock_many_days
from kit.sql_api.common import create_checker
from datetime import datetime, timedelta
from os import system
from time import sleep





def create_quotes_and_fill_by_ticker(path_to_db: str, days_delta: int, interval: str, sleep_sec: int):
    __doc__ = "interval is 5m or 15m"
    print("quotes db initialize")
    try:
        create_checker(path_to_db)

        for ticker in ticker_to_figi:
            if create_ticker_table_in_quotes(ticker, path_to_db):
                print(ticker, "table created")
                date_from = datetime.now() - timedelta(days=days_delta)
                df = get_df_from_stock_many_days(figi=ticker_to_figi[ticker], interval=interval, date1=date_from,
                                       date2=datetime.now())
                print(df)
                if df:
                    put_df_to_db(df, ticker, path_to_db)
                    print(ticker, "status: loaded", len(df.index), "rows")
                else:
                    print(ticker, "status: no data to put")
                sleep(sleep_sec)
        return True
    except Exception as e:
        print("Error while initializing on step", ticker, e)
        return False


def init_quotes_with_system_commands(path_to_db, days_delta, interval, sleep_sec):
    buffer_mark = "_buffer"
    delete_command = f"rm {path_to_db}"
    delete_buf_command = f"rm {path_to_db}{buffer_mark}"
    move_command = f"mv {path_to_db}{buffer_mark} {path_to_db}"
    system(delete_buf_command)
    if create_quotes_and_fill_by_ticker(f"{path_to_db}{buffer_mark}", days_delta, interval, sleep_sec):
        system(delete_command)
        system(move_command)
