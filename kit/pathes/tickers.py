from pathlib import Path


dirname = Path.dirname(__file__).parents[0]

path_full_moex = Path.join(dirname, 'catalog', 'full_moex')
path_short_moex = Path.join(dirname, 'catalog', 'short_moex')