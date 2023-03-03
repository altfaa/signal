import os
pwd = os.getcwd()
dirname = os.path.dirname(__file__)


DB_NAME_QUOTES_1H = os.path.join(dirname, '../db/quotes.db')
DB_NAME_QUOTES_15M = os.path.join(dirname, '../db/quotes_15.db')
DB_NAME_QUOTES_5M = os.path.join(dirname, '../db/quotes_5.db')

