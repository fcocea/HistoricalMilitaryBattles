import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

battles = pd.read_csv('data/battles_clean.csv')
conflicts = battles[['isqno', 'attacker', 'defender']]
conflicts = conflicts.groupby(['attacker', 'defender']).count()
conflicts = conflicts.rename(columns={'isqno': 'count'})
conflicts = conflicts.sort_values('count', ascending=False)
conflicts = conflicts.reset_index()
# countries sin repetir
countries = pd.concat([conflicts['attacker'], conflicts['defender']]).unique()
# ordenar por nombre
countries = np.sort(countries)

df_results = pd.DataFrame(columns=['country', 'won', 'lost', 'draws'])
df_results['country'] = countries

# ver si los paises de df_results estan en una fila de battles y si ganaron o perdieron, si son attacker y winner 
# is attacker won +1, si son defender y winner is defender +1 si es attacker o defender y winner es otro lost +1

for index, row in df_results.iterrows():
    country = row['country']
    won = 0
    lost = 0
    draws = 0
    for index, row in battles.iterrows():
        if row['attacker'] == country:
            if row['winner'] == 'attacker':
                won += 1
            elif row['winner'] == 'defender':
                lost += 1
            else:
                draws += 1
        elif row['defender'] == country:
            if row['winner'] == 'defender':
                won += 1
            elif row['winner'] == 'attacker':
                lost += 1
            else:
                draws += 1
                
            
    df_results.loc[df_results['country'] == country, 'won'] = won
    df_results.loc[df_results['country'] == country, 'lost'] = lost
    df_results.loc[df_results['country'] == country, 'draws'] = draws

# calcular porcentaje de victorias , derrote y empates
df_results['total'] = df_results['won'] + df_results['lost'] + df_results['draws']
df_results['won_percentage'] = df_results['won'] / df_results['total']
df_results['lost_percentage'] = df_results['lost'] / df_results['total']
df_results['draws_percentage'] = df_results['draws'] / df_results['total']

# multiplicar por 100 y aproximar a 2 decimales
df_results['won_percentage'] = df_results['won_percentage'] * 100
df_results['lost_percentage'] = df_results['lost_percentage'] * 100
df_results['draws_percentage'] = df_results['draws_percentage'] * 100
