import pandas as pd
import numpy as np
from dash_manager import app
from dash import Output, Input
import plotly.graph_objects as go

troops = pd.read_csv('data/battles_clean.csv')
troops = troops[['isqno', 'date_start', 'attacker',
                 'defender','a_aircraft', 'a_artillery', 'a_cavalry', 'a_tanks', 'd_aircraft', 'd_artillery', 'd_cavalry','d_tanks']]
countries = troops['attacker'].unique()
countries = np.append(countries, troops['defender'].unique())
countries = np.unique(countries)


@app.callback(
    [Output('battle-troops', 'figure'),
     Output('battle-troops-title', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_battle_troops(selected_country):
    isAttacker = False
    if (troops['attacker'] == selected_country):
        isAttacker = True
    filtered_troops = troops[(troops['attacker'] == selected_country) | (
        troops['defender'] == selected_country)].copy()
    if isAttacker:
        filtered_troops.drop(
        columns=['attacker', 'defender', 'date_start', 'isqno', 'd_tanks', 'd_artillery', 'd_cavalry', 'd_aircraft'], inplace=True)
        filtered_troops.rename(columns={'a_tanks': 'tanks', 'a_artillery': 'artillery', 'a_cavalry': 'cavalry', 'a_aircraft': 'aircraft'}, inplace=True)
    else:
        filtered_troops.drop(
            columns=['attacker', 'defender', 'date_start', 'isqno', 'a_tanks', 'a_artillery', 'a_cavalry', 'a_aircraft'], inplace=True)
        filtered_troops.rename(columns={'d_tanks': 'tanks', 'd_artillery': 'artillery', 'd_cavalry': 'cavalry', 'd_aircraft': 'aircraft'}, inplace=True)
    filtered_troops = filtered_troops.transpose()
    filtered_troops['Total'] = filtered_troops.sum(axis=1)
    filtered_troops = filtered_troops[['Total']]
    total_values = sum(filtered_troops['Total'])
    category_proportions = {category: float(
        value) / total_values for category, value in zip(filtered_troops.index, filtered_troops['Total'])}
    width = 30
    height = 20
    total_num_tiles = width * height

    category_tiles = {category: round(proportion * total_num_tiles)
                      for category, proportion in category_proportions.items()}
    category_tiles = dict(sorted(category_tiles.items(),
                          key=lambda item: item[1], reverse=True))

    max_category = max(category_tiles, key=category_tiles.get)
    if sum(category_tiles.values()) < total_num_tiles:
        category_tiles[max_category] += total_num_tiles - \
            sum(category_tiles.values())
    elif sum(category_tiles.values()) > total_num_tiles:
        category_tiles[max_category] -= sum(
            category_tiles.values()) - total_num_tiles

    # inicializa el waffle chart como una matriz vacía
    waffle_chart = np.zeros((height, width))

    categories = ['aircraft', 'artillery', 'cavalry', 'tanks']
    z_values = {
        'aircraft': 0,
        'artillery': 1,
        'cavalry': 2,
        'tanks': 3
    }
    # Definición de la escala de colores
    color_map = {
        'aircraft': '#66C2A5',
        'artillery': '#FC8D62',
        'cavalry': '#8DA0CB',
        'tanks': '#E78AC3'
    }

    colorscale = [
        [0.00, color_map['aircraft']],  # color para el valor 1
        [0.25, color_map['aircraft']],
        [0.25, color_map['artillery']],   # color para el valor 2
        [0.50, color_map['artillery']],
        [0.50, color_map['cavalry']],  # color para el valor 3
        [0.75, color_map['cavalry']],
        [0.75, color_map['tanks']],  # color para el valor 4
        [1.00, color_map['tanks']]
    ]

    translate_troop = {
        'aircraft': 'Aéreo',
        'artillery': 'Artilleria',
        'cavalry': 'Caballería',
        'tanks': 'Tanques'
    }

    tile_index = 0
    category_index = 0

    for col in range(width):
        for row in range(height):
            tile_index += 1

            if tile_index > sum(list(category_tiles.values())[0:category_index]):
                category_index += 1

            waffle_chart[row, col] = z_values[list(
                category_tiles)[category_index-1]]

    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=waffle_chart,
        zmin=0,
        zmax=3,
        colorscale=colorscale,
        xgap=2,
        ygap=2,
        showscale=False,
        hoverinfo='skip'
    ))

    # Añadir trazos de Scatter para la leyenda utilizando colores específicos de category_color_map
    for category in categories:
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            # Usa el color específico para cada categoría
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
            xanchor='right',
            x=0.7,
            font=dict(size=14)
        )
    )

    fig.update_layout(
        # title=f'Waffle Chart for {selected_country}',
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return [fig, f'Waffle Chart {selected_country}']
