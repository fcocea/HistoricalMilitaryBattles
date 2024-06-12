import pandas as pd

battles_clean = pd.read_csv('data/battles_clean.csv')

battles = pd.read_csv('data/battles.csv')
battles = battles[['isqno', 'locn']]

locn = pd.merge(battles_clean, battles, on='isqno', how='inner')
locn.to_csv('data/battles_clean.csv', index=False)
