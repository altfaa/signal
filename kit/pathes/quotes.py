from pathlib import Path

dirname = Path(__file__).parents[2]

DB_NAME_QUOTES_1H = Path(dirname, 'db', 'quotes.db')
DB_NAME_QUOTES_15M = Path(dirname, 'db', 'quotes_15.db')
DB_NAME_QUOTES_5M = Path(dirname, 'db', 'quotes_5.db')

print(DB_NAME_QUOTES_5M)
