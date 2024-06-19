import numpy as np
import pandas as pd
import plotly.graph_objs as go

from dash_manager import app
from dash import Output, Input

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

@app.callback(
    [Output('graph', 'figure'),
     Output('pie-chart', 'figure'), Output('graph-title', 'children'), Output('pie-chart-title', 'children')],
    [Input('country-dropdown', 'value'),
     Input('contrincante-dropdown', 'value')]
)
def update_graph(selected_country, selected_contrincante=None):
    if selected_contrincante is None:
        # Gráfico de barras para ataques y defensas
        df_attacks = conflicts[conflicts['defender'] == selected_country]
        df_defenses = conflicts[conflicts['attacker'] == selected_country]

        # Conjunto de todos los países involucrados en ataques o defensas
        all_countries = set(df_attacks['attacker']).union(
            set(df_defenses['defender']))

        # Datos de defensa y ataque para todos los países
        defense_data = {country: -df_attacks.loc[df_attacks['attacker']
                                                == country, 'count'].sum() for country in all_countries}
        attack_data = {country: df_defenses.loc[df_defenses['defender'] == country, 'count'].sum(
        ) for country in all_countries}

        # Crear el gráfico de barras
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=list(defense_data.keys()),
            x=list(defense_data.values()),
            name='Defiende',
            marker_color='blue',
            orientation='h',
            text=[-1 * x if x != 0 else None for x in defense_data.values()],
            textposition="outside"
        ))
        fig.add_trace(go.Bar(
            y=list(attack_data.keys()),
            x=list(attack_data.values()),
            name='Ataca',
            marker_color='red',
            orientation='h',
            yaxis='y2',
            text=[x if x != 0 else None for x in attack_data.values()],
            textposition="outside"
        ))
        fig.update_layout(
            # title=f'Conflictos que involucran a {selected_country}',
            xaxis_title='Número de batallas',
            yaxis_title='Defiende',
            yaxis2=dict(
                title='Ataca',
                overlaying='y',
                side='right'
            ),
            barmode='relative',
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation='h', yanchor='bottom',
                        y=1.02, xanchor='center', x=0.5)
        )
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_traces(hoverinfo='skip')

        df_selected = df_results[df_results['country'] == selected_country]
        pie_fig = go.Figure(data=[go.Pie(
            labels=['Ganadas', 'Perdidas', 'Empatadas'],
            values=[df_selected['won'].values[0],
                    df_selected['lost'].values[0], df_selected['draws'].values[0]],
            hole=.4,
            hoverinfo='label+percent',
            marker=dict(colors=['red', 'blue', 'gray']),
            textfont=dict(color='white'),
            hoverlabel=dict(font=dict(color='white'))
        )])
        # remove hover
        pie_fig.update_traces(hoverinfo='skip')
        pie_fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            # title=f'Porcentaje de Resultados de Batallas para {selected_country}',
            legend=dict(orientation='h', yanchor='bottom',
                        y=1, xanchor='right', x=0.66),
        )
        pie_fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        return [fig, pie_fig, f'Conflictos que involucran a {selected_country}', f'Porcentaje de Resultados de Batallas para {selected_country}']
    else:
        battles = pd.read_csv('data/battles_clean.csv')
        df_conflicts = battles[['isqno', 'attacker', 'defender','winner']]
        df_conflicts = df_conflicts.set_index(['isqno']) 

        country1 = selected_country
        df_conflicts = df_conflicts[(df_conflicts['attacker'] == country1) | (df_conflicts['defender'] == country1)]

        country2 = selected_contrincante
        df_conflicts = df_conflicts[(df_conflicts['attacker'] == country2) | (df_conflicts['defender'] == country2)]

        for index, row in df_conflicts.iterrows():
            if row['winner'] == 'attacker':
                df_conflicts.at[index, 'country_winner'] = row['attacker']
            elif row['winner'] == 'defender':
                df_conflicts.at[index, 'country_winner'] = row['defender']
            else:
                df_conflicts.at[index, 'country_winner'] = 'draw'
            
        
        conflict_count = df_conflicts['attacker'].value_counts().to_frame().reset_index()
        conflict_count.columns = ['country', 'attacker_count']
        conflict_count = conflict_count.sort_values(by='attacker_count', ascending=False)
        attacks_count = conflict_count[conflict_count['country'] == country1]
        defends_count = conflict_count[conflict_count['country'] == country2]
        try:
            attack_data2 = {country2: attacks_count['attacker_count'].values[0]}
        except:
            attack_data2 = {country2: 0}
        try:
            defense_data2 = {country2: -defends_count['attacker_count'].values[0]}
        except:
            defense_data2 = {country2: 0}

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=list(defense_data2.keys()),
            x=list(defense_data2.values()),
            name='Defiende',
            marker_color='blue',
            orientation='h',
            text=[-1 * x if x != 0 else None for x in defense_data2.values()],
            textposition="outside"
        ))
        fig.add_trace(go.Bar(
            y=list(attack_data2.keys()),
            x=list(attack_data2.values()),
            name='Ataca',
            marker_color='red',
            orientation='h',
            yaxis='y2',
            text=[x if x != 0 else None for x in attack_data2.values()],
            textposition="outside"
        ))
        fig.update_layout(
            # title=f'Conflictos que involucran a {selected_country}',
            xaxis_title='Número de batallas',
            yaxis_title='Defiende',
            yaxis2=dict(
                title='Ataca',
                overlaying='y',
                side='right'
            ),
            barmode='relative',
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation='h', yanchor='bottom',
                        y=1.02, xanchor='center', x=0.5)
        )
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        wins = df_conflicts.groupby(['country_winner']).size().reset_index(name='wins')
        wins = wins.rename(columns={'country_winner': 'country'})
        try:
            win_data = {country1: wins[wins['country'] == country1]['wins'].values[0]}
        except:
            win_data = {country1: 0}
        try:
            lose_data = {country2: wins[wins['country'] == country2]['wins'].values[0]}
        except:
            lose_data = {country2: 0}
        if 'draw' in wins['country'].values:
            draw_data = {'draw': wins[wins['country'] == 'draw']['wins'].values[0]}
        else:
            draw_data = {'draw': 0}
        pie_fig = go.Figure(data=[go.Pie(
            labels=['Ganadas', 'Perdidas', 'Empatadas'],
            values=[win_data[country1], lose_data[country2], draw_data['draw']],
            hole=.4,
            hoverinfo='label+percent',
            marker=dict(colors=['red', 'blue', 'gray']),
            textfont=dict(color='white'),
            hoverlabel=dict(font=dict(color='white'))
        )])
        # remove hover
        pie_fig.update_traces(hoverinfo='skip')
        pie_fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            # title=f'Porcentaje de Resultados de Batallas para {selected_country}',
            legend=dict(orientation='h', yanchor='bottom',
                        y=1, xanchor='right', x=0.66),
        )
        pie_fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        return [fig, pie_fig, f'Conflictos que involucran a {selected_country} contra {selected_contrincante}', f'Porcentaje de Resultados de Batallas para {selected_country} contra {selected_contrincante}']