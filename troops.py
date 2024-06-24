import pandas as pd
import numpy as np
from dash_manager import app
from dash import Output, Input
import plotly.graph_objects as go

def create_waffle_chart(data, height, width, categories, colorscale, selected_country, y_offset):
    total_values = sum(data['Total'])
    category_proportions = {category: float(value) / total_values for category, value in zip(data.index, data['Total'])}
    total_num_tiles = width * height
    category_tiles = {category: round(proportion * total_num_tiles) for category, proportion in category_proportions.items()}
    category_tiles = dict(sorted(category_tiles.items(), key=lambda item: item[1], reverse=True))

    max_category = max(category_tiles, key=category_tiles.get)
    if sum(category_tiles.values()) < total_num_tiles:
        category_tiles[max_category] += total_num_tiles - sum(category_tiles.values())
    elif sum(category_tiles.values()) > total_num_tiles:
        category_tiles[max_category] -= sum(category_tiles.values()) - total_num_tiles

    waffle_chart = np.zeros((height, width))
    tile_index = 0
    category_index = 0

    z_values = {category: i for i, category in enumerate(categories)}
    for col in range(width):
        for row in range(height):
            tile_index += 1
            if tile_index > sum(list(category_tiles.values())[0:category_index]):
                category_index += 1
            waffle_chart[row, col] = z_values[list(category_tiles)[category_index-1]]
    
    return go.Heatmap(
        z=waffle_chart,
        x0=0, dx=1, y0=y_offset, dy=1,  # Comienza en y0=y_offset
        colorscale=colorscale,
        xgap=2,
        ygap=2,
        showscale=False,
        hoverinfo='skip',
        name=selected_country,
        zmin=0,
        zmax=3
    )

battles = pd.read_csv('data/battles_clean.csv')
df_belligerents = pd.read_csv('data/belligerents.csv')


@app.callback(
    [Output('battle-troops', 'figure'),
     Output('battle-troops-title', 'children')],
    [Input('country-dropdown', 'value'),
     Input('contrincante-dropdown', 'value')]
)
def update_battle_troops(selected_country, selected_contrincante=None):
    if selected_contrincante is None:
        troops = battles[((battles['attacker'] == selected_country) | (battles['defender'] == selected_country))]
        troops = troops[['isqno', 'attacker', 'defender', 'date_start']]
        troops['date_start'] = pd.to_datetime(troops['date_start'])
        troops = troops.merge(df_belligerents, on='isqno')
        troops['country'] = np.where(troops['attacker_y'] == 1, troops['attacker_x'], troops['defender'])
        troops.drop(['attacker_x', 'defender', 'attacker_y'], axis=1, inplace=True)

        troops = troops[troops['country'] == selected_country]
        troops = troops[['country','tank', 'arty', 'fly', 'cav']]
        troops.columns = ['country', 'tanks', 'artillery', 'aircraft', 'cavalry']

        troops = troops.groupby(['country']).sum().reset_index()
        troops = troops.drop('country', axis=1)
        troops = troops.transpose()

        troops.columns = ['Total']

        categories = ['aircraft', 'artillery', 'cavalry', 'tanks']
        color_map = {
            'aircraft': '#66C2A5',
            'artillery': '#FC8D62',
            'cavalry': '#8DA0CB',
            'tanks': '#E78AC3'
        }
        colorscale = [
            [0.00, color_map['aircraft']],  # color para el valor 1
            [0.249, color_map['aircraft']],
            [0.25, color_map['artillery']],   # color para el valor 2
            [0.499, color_map['artillery']],
            [0.50, color_map['cavalry']],  # color para el valor 3
            [0.749, color_map['cavalry']],
            [0.75, color_map['tanks']],  # color para el valor 4
            [1.00, color_map['tanks']]
        ]

        translate_troop = {
            'aircraft': 'Aéreo',
            'artillery': 'Artilleria',
            'cavalry': 'Caballería',
            'tanks': 'Tanques'
        }
        fig = go.Figure()
        fig_country = create_waffle_chart(troops, 20, 30, categories, colorscale, selected_country, y_offset=0)
        fig.add_trace(fig_country)
        for category in categories:
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(size=12, color=color_map[category]),
                legendgroup=category,
                showlegend=True,
                name=translate_troop[category]
            ))
        fig.update_layout(
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
        )

        return [fig, f'Proporción de tropas en batallas que involucran a {selected_country}']
    else:
        troops = battles[((battles['attacker'] == selected_country) & (battles['defender'] == selected_contrincante)) |
                        ((battles['attacker'] == selected_contrincante) & (battles['defender'] == selected_country))]
        troops = troops[['isqno', 'attacker', 'defender', 'date_start']]
        troops['date_start'] = pd.to_datetime(troops['date_start'])
        troops = troops.merge(df_belligerents, on='isqno')

        troops['country'] = np.where(troops['attacker_y'] == 1, troops['attacker_x'], troops['defender'])
        troops.drop(['attacker_x', 'defender', 'attacker_y'], axis=1, inplace=True)

        troops = troops[['country','tank', 'arty', 'fly', 'cav']]
        # rename columns tank a tanks, arty a artillery, fly a aircraft, cav a cavalry
        troops.columns = ['country', 'tanks', 'artillery', 'aircraft', 'cavalry']

        troops = troops.groupby(['country']).sum().reset_index()
        # añadir columna total
        #troops['total'] = troops['tank'] + troops['arty'] + troops['fly'] + troops['cav']
        troops_attacker = troops[troops['country'] == selected_country]
        troops_defender = troops[troops['country'] == selected_contrincante]
        # quitamos la columna country
        troops_attacker = troops_attacker.drop('country', axis=1)
        troops_defender = troops_defender.drop('country', axis=1)

        troops_attacker = troops_attacker.transpose()
        troops_defender = troops_defender.transpose()

        troops_attacker.columns = ['Total']
        troops_defender.columns = ['Total']
        categories = ['aircraft', 'artillery', 'cavalry', 'tanks']
        color_map = {
            'aircraft': '#66C2A5',
            'artillery': '#FC8D62',
            'cavalry': '#8DA0CB',
            'tanks': '#E78AC3'
        }
        colorscale = [
            [0.00, color_map['aircraft']],  # color para el valor 1
            [0.249, color_map['aircraft']],
            [0.25, color_map['artillery']],   # color para el valor 2
            [0.499, color_map['artillery']],
            [0.50, color_map['cavalry']],  # color para el valor 3
            [0.749, color_map['cavalry']],
            [0.75, color_map['tanks']],  # color para el valor 4
            [1.00, color_map['tanks']]
        ]

        translate_troop = {
            'aircraft': 'Aéreo',
            'artillery': 'Artilleria',
            'cavalry': 'Caballería',
            'tanks': 'Tanques'
        }

        fig = go.Figure()

        # Añadir el waffle chart del atacante con un desplazamiento de y=0
        fig_attacker = create_waffle_chart(troops_attacker, 10, 40, categories, colorscale, selected_country, y_offset=0)
        fig.add_trace(fig_attacker)

        # Añadir el waffle chart del defensor con un desplazamiento de y=-11 (ajuste según la necesidad)
        fig_defender = create_waffle_chart(troops_defender, 10, 40, categories, colorscale, selected_contrincante, y_offset=-11)
        fig.add_trace(fig_defender)
        fig.add_annotation(
            x=0.5, y=0.5, xref='paper', yref='paper',
            showarrow=False, text=f"{selected_country}", font=dict(size=14, color='black'), bgcolor='rgba(255,255,255,0.8)')

        fig.add_annotation(
            x=0.5, y=1.03, xref='paper', yref='paper',
            showarrow=False, text=f"{selected_contrincante}", font=dict(size=14, color='black'), bgcolor='rgba(255,255,255,0.8)')

        for category in categories:
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(size=12, color=color_map[category]),
                legendgroup=category,
                showlegend=True,
                name=translate_troop[category]
            ))

        fig.update_layout(
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
        )

        return [fig, f'Proporción de tropas en las batallas de {selected_country} contra {selected_contrincante}']
