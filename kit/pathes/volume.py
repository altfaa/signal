from pathlib import Path


dirname = Path.dirname(__file__).parents[1]

DB_NAME_VOLUMER_1H  = Path.join(dirname, 'db', 'volumer.db')
DB_NAME_VOLUMER_15M = Path.join(dirname, 'db', 'volumer_15.db')