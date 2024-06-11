from dash import Dash, html, dcc, callback, Output, Input
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
from dash.exceptions import PreventUpdate
from conflicts import df_results, conflicts, countries
from dash.dependencies import Input, Output
import plotly.graph_objects as go

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(__name__, external_stylesheets=stylesheets)

years = [{"value": year, "label": year} for year in range(1600, 1974, 50)] + [{"value": 1973, "label": 1973}]

def get_layout():
    return dmc.MantineProvider(html.Div([
    html.Div([
        dmc.Title("Batallas militares históricas", order=1),
        dmc.Text("Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.", size="sm"),
    ], className="title-container"),
    html.Div(
    [
       dmc.RangeSlider(
            id="range-slider-callback",
            marks=years,
            max=1973,
            min=1600,
            mb=35,
            minRange=25,
            labelAlwaysOn=True,
            value=[1600,1973]
        ),
        dmc.Space(h=10),
        dmc.Text(id="range-slider-output"),
    ]
    ),
    dmc.Select(
        id='country-dropdown',
        data=countries,
        searchable=True,
        value='USA',
    ),
    dmc.Flex([
        dcc.Graph(id='graph',responsive=True),
        dcc.Graph(id='pie-chart', responsive=True)
    ], direction={"base": "column", "sm": "row"}, w={"base": "100%", "sm": "100%"}, gap="lg")
]))

@callback(
    Output("range-slider-output", "children"), Input("range-slider-callback", "value")
)
def update_value(value):
    return f"You have selected: [{value[0]}, {value[1]}]"
    
app.layout = get_layout

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
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5)
    )
    pie_fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig, pie_fig

if __name__ == '__main__':
    app.run(debug=True)
