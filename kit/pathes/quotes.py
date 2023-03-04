from pathlib import Path


dirname = Path.dirname(__file__).parents[1]

DB_NAME_QUOTES_1H  = Path.join(dirname, 'db', 'quotes.db')
DB_NAME_QUOTES_15M = Path.join(dirname, 'db', 'quotes_15.db')
DB_NAME_QUOTES_5M  = Path.join(dirname, 'db', 'quotes_5.db')

