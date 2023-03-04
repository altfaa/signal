from kit.catalog.get_dicts import get_dict
from kit.pathes.tickers import path_full_moex

name_to_figi_dict, figi_to_name_dict, figi_to_ticker, ticker_to_figi, ticker_to_name = \
    get_dict(path_full_moex)

