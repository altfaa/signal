import sqlite3 as sl

def create_checker(db_name):
    con = sl.connect(db_name)
    str_com = """
        CREATE TABLE CHECKER (
            Name TEXT,
            Last TEXT
        );
    """
    with con:
        try:
            con.execute(str_com)
            con.commit()
        except Exception as e:
            print(e)
            return f"error: {e}"
    return "ok"


def insert_first_row_to_checker(ticker, date, db_path):
    con = sl.connect(db_path)

    with con:
        try:
            data = con.execute(f"SELECT * FROM CHECKER WHERE Name = '{ticker}'")
            for row in data:
                return f"{ticker} row already exist"
            data = con.execute(f"INSERT INTO CHECKER (Name, Last) VALUES ('{ticker}','{date}')")
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False

def create_checker(db_name):
    con = sl.connect(db_name)
    str_com = """
        CREATE TABLE CHECKER (
            Name TEXT,
            Last TEXT
        );
    """
    with con:
        try:
            con.execute(str_com)
            con.commit()
        except Exception as e:
            print(e)
            return f"error: {e}"
    return "ok"

def create_ticker_table_in_quotes(ticker, db_path):
    try:
        con = sl.connect(db_path)

        with con:
            con.execute(f"""
            CREATE TABLE {ticker} (            
                Date TEXT,
                Open TEXT,            
                High TEXT,
                Low TEXT,
                Close TEXT,
                Volume TEXT
                );
            """)
            con.commit()

        insert_first_row_to_checker(ticker, '2000-01-01 00:00', db_path)
        return True
    except Exception as e:
        print(e)
        return False


def update_date_in_checker(ticker, date, db_path):
    con = sl.connect(db_path)

    with con:
        try:
            data = con.execute(f"UPDATE CHECKER set Last = '{date}' WHERE Name = '{ticker}'")
            con.commit()
        except Exception as e:
            print(e)
            return f"error: {e}"
    return "ok"


def get_date_from_checker(ticker, db_path):
    con = sl.connect(db_path)

    last_date = "empty"
    with con:
        try:
            data = con.execute(f"SELECT Last FROM CHECKER WHERE Name = '{ticker}'")
            for row in data:
                last_date = row[0]
        except Exception as e:
            print(e)
            return last_date
    return last_date


def put_df_to_db(df, ticker, db_path):
    try:
        last_date = get_date_from_checker(ticker, db_path)
        print("last date", last_date)

        con = sl.connect(db_path)

        with con:
            inserted_count = df.loc[(df['Date'] > last_date)].to_sql(name=ticker, con=con, if_exists='append',
                                                                     index=False)

            print("inserted_count:", inserted_count)
            con.commit()
            if inserted_count != 0:
                update_date_in_checker(ticker, df['Date'].max(), db_path)
        return f"OK. Inserted {inserted_count} rows"
    except Exception as e:
        print(e)
        return f"error: {e}"


def create_table_and_fill_by_ticker(ticker, path_to_db, df):

    if create_ticker_table_in_quotes(ticker, path_to_db):
        put_df_to_db(df, ticker, path_to_db)

    print(ticker, "loaded")

