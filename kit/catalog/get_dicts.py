from pandas import read_csv


def get_dict(path):
    name_to_figi_dict = {}
    figi_to_name_dict = {}
    figi_to_ticker = {}
    ticker_to_figi = {}
    ticker_to_name = {}

    df = read_csv(path, sep=";", header=None, skipinitialspace=True)
    df.columns = ['ticker', 'figi', 'name']
    df['ticker'] = df['ticker'].str.strip()
    df['figi'] = df['figi'].str.strip()
    df['name'] = df['name'].str.strip()

    for index, row in df.sort_values('ticker').iterrows():
        name = row['name']
        figi = row['figi']
        ticker = row['ticker']

        name_to_figi_dict[name] = figi
        figi_to_name_dict[figi] = name
        figi_to_ticker[figi] = ticker
        ticker_to_figi[ticker] = figi
        ticker_to_name[ticker] = name

    return name_to_figi_dict[name], figi_to_name_dict[figi], figi_to_ticker[figi],  ticker_to_figi[ticker],  ticker_to_name[ticker]
