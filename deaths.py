import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash_manager import app
from dash import  Output, Input

deaths = pd.read_csv('data/battles_clean.csv')
deaths = deaths[['isqno','date_start', 'attacker', 'defender', 'deaths']]

@app.callback(
    Output('boxplot_deaths', 'figure'),
    [Input('country-dropdown', 'value')]
)
def boxplot_deaths(selected_country):
    deaths_country = deaths.loc[(deaths['attacker'] == selected_country) | (deaths['defender'] == selected_country)].copy()
    deaths_country.loc[:, 'year'] = pd.to_datetime(deaths_country['date_start']).dt.year
    deaths_country = deaths_country[['year', 'deaths']]
    deaths_country = deaths_country.groupby('year').sum().reset_index()

    deaths_country = deaths_country.set_index('year')

    deaths_country.columns = [selected_country]
    fig = px.box(deaths_country, x=selected_country, orientation='h', title='Box plot de muertes de ' + selected_country, labels={selected_country: 'Muertes'})

    # Update y-axis label
    fig.update_yaxes(title_text=selected_country)

    return fig