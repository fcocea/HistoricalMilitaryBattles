import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash_manager import app
from dash import Output, Input

deaths = pd.read_csv('data/battles_clean.csv')
deaths = deaths[['isqno', 'date_start', 'attacker', 'defender', 'deaths']]


@app.callback(
    [Output('boxplot_deaths', 'figure'), Output(
        'boxplot-deaths-title', 'children')],
    [Input('country-dropdown', 'value')]
)
def boxplot_deaths(selected_country):
    deaths_country = deaths.loc[(deaths['attacker'] == selected_country) | (
        deaths['defender'] == selected_country)].copy()
    deaths_country.loc[:, 'year'] = pd.to_datetime(
        deaths_country['date_start']).dt.year
    deaths_country = deaths_country[['year', 'deaths']]
    deaths_country = deaths_country.groupby('year').sum().reset_index()

    deaths_country = deaths_country.set_index('year')

    deaths_country.columns = [selected_country]
    fig = px.box(deaths_country, x=selected_country,
                 orientation='h', labels={selected_country: 'Muertes'})
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    fig.update_xaxes(showgrid=False, showline=False)
    fig.update_yaxes(showgrid=False, showline=False)

    fig.update_yaxes(title_text=selected_country)
    fig.update_traces(hoverinfo='none')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(hovermode=False)
    return [fig, f"Distribución de las muertes en batalla que involucran a {selected_country}"]
