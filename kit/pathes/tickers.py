from pathlib import Path


dirname = Path(__file__).parents[1]

path_full_moex = Path(dirname, 'catalog', 'full_moex')
path_short_moex = Path(dirname, 'catalog', 'short_moex')
print(dirname)
print(path_full_moex)