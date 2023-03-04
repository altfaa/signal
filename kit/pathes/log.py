from pathlib import Path


dirname = Path.dirname(__file__).parents[1]

LOG_TO_REGULAR_FILL_15M = Path.join(dirname, 'log', 'log_regular_fill_15m')
LOG_TO_REGULAR_FILL_5M =  Path.join(dirname, 'log', 'log_regular_fill_5m')
LOG_TO_REGULAR_FILL_1H =  Path.join(dirname, 'log', 'log_regular_fill_1h')