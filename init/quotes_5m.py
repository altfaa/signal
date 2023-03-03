from kit.sql_api.init.quotes import init_quotes_with_system_commands
from kit.pathes.quotes import DB_NAME_QUOTES_5M

init_quotes_with_system_commands(path_to_db=DB_NAME_QUOTES_5M, days_delta=7, interval="5m", sleep_sec=1)
