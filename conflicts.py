import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

from dash_manager import app
from dash import  Output, Input

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

@app.callback(
    [Output('graph', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_graph(selected_country):
    # Gráfico de barras para ataques y defensas
    df_attacks = conflicts[conflicts['defender'] == selected_country]
    df_defenses = conflicts[conflicts['attacker'] == selected_country]

    # Conjunto de todos los países involucrados en ataques o defensas
    all_countries = set(df_attacks['attacker']).union(set(df_defenses['defender']))

    # Datos de defensa y ataque para todos los países
    defense_data = {country: -df_attacks.loc[df_attacks['attacker'] == country, 'count'].sum() for country in all_countries}
    attack_data = {country: df_defenses.loc[df_defenses['defender'] == country, 'count'].sum() for country in all_countries}

    # Crear el gráfico de barras
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=list(defense_data.keys()),
        x=list(defense_data.values()),
        name='Defiende',
        marker_color='blue',
        orientation='h'
    ))
    fig.add_trace(go.Bar(
        y=list(attack_data.keys()),
        x=list(attack_data.values()),
        name='Ataca',
        marker_color='red',
        orientation='h',
        yaxis='y2'
    ))
    fig.update_layout(
        title=f'Conflictos que involucran a {selected_country}',
        xaxis_title='Número de batallas',
        yaxis_title='Defiende',
        yaxis2=dict(
            title='Ataca',
            overlaying='y',
            side='right'
        ),
        barmode='relative',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    df_selected = df_results[df_results['country'] == selected_country]
    pie_fig = go.Figure(data=[go.Pie(
        labels=['Ganadas', 'Perdidas', 'Empatadas'],
        values=[df_selected['won'].values[0], df_selected['lost'].values[0], df_selected['draws'].values[0]],
        hole=.4,
        hoverinfo='label+percent',
        marker=dict(colors=['red', 'blue', 'gray']),
        textfont=dict(color='white'),
        hoverlabel=dict(font=dict(color='white'))
    )])
    pie_fig.update_layout(
        title=f'Porcentaje de Resultados de Batallas para {selected_country}',
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.66),
    )
    pie_fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig, pie_fig
