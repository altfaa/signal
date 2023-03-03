from kit.catalog.get_full_moex_dicts import ticker_to_figi
from kit.pathes.log import LOG_TO_REGULAR_FILL_5M
from kit.pathes.quotes import DB_NAME_QUOTES_5M
from kit.stock_api.quotes.get_df import get_df_from_stock
from kit.sql_api.common import put_df_to_db, get_date_from_checker
from datetime import datetime, timedelta
from time import sleep
from kit.sql_api.init.quotes import init_quotes_with_system_commands

message = f"unreachable message"
# regular fill for 5min db
for ticker in ticker_to_figi:
    try:
        last_date_in_db_str = get_date_from_checker(ticker, DB_NAME_QUOTES_5M)
        last_date_in_db_datetype = datetime.strptime(last_date_in_db_str, '%Y-%m-%d %H:%M')
        db_delta = datetime.now() - last_date_in_db_datetype
        date_from = datetime.now()

        now_day = datetime.now().day
        db_min = last_date_in_db_datetype.min
        db_hour = last_date_in_db_datetype.hour
        db_day = last_date_in_db_datetype.day

        # not first fill in day
        if db_day == now_day:
            # basic case - next fill
            if db_delta < timedelta(minutes=10):
                date_from -= timedelta(minutes=10)
            elif db_delta < timedelta(minutes=30):
                date_from -= timedelta(minutes=30)
            elif db_delta < timedelta(hours=2):
                date_from -= timedelta(hours=2)
                sleep(1)
            elif db_delta < timedelta(hours=6):
                date_from -= timedelta(hours=6)
                sleep(3)
            # if failure in internet connection or server or info-host
            elif db_delta < timedelta(hours=12):
                date_from -= timedelta(hours=12)
                sleep(5)
        else:
            # first fill in day
            if (db_hour == 22 and db_min == 45) or (db_hour == 18 and db_min == 45):
                date_from -= timedelta(hours=2)
            else:  # outdated data in db, need to reload db
                init_quotes_with_system_commands(path_to_db=DB_NAME_QUOTES_5M, days_delta=7, interval="5m",
                                                 sleep_sec=1)
                date_from = False

        if date_from:
            df = get_df_from_stock(figi=ticker_to_figi[ticker], interval="5m", date_start=date_from,
                                   date_end=datetime.now())
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            status = put_df_to_db(df=df, ticker=ticker, db_path=DB_NAME_QUOTES_5M)
            message = f"{time} Регулярная выгрузка. Статус: {status} {ticker}"
            print(message)
        else:
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            message = f"{time} BD reloaded. Reason: outdated data. {DB_NAME_QUOTES_5M}"

    except Exception as e:
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"{time} Error on step: {ticker}: {e}.\n"
        with open(LOG_TO_REGULAR_FILL_5M, "a") as f:
            f.write(message)
        raise Exception(e)

with open(LOG_TO_REGULAR_FILL_5M, "a") as f:
    f.write(message)
