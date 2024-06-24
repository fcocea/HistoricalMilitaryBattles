from dash_manager import app
from dash import Output, Input, State, no_update
import pandas as pd
from dash.exceptions import PreventUpdate

battles = pd.read_csv('data/battles_clean.csv')
battles['year'] = battles['date_start'].str.extract(r'(\d{4})')
battles['year'] = battles['year'].astype(int)


@app.callback(
    [Output('country-dropdown', 'data'), Output('country-dropdown', 'value')],
    [Input('range-slider', 'value')],
    [State('country-dropdown', 'value')]
)
def update_countries(value, country):
    start, end = value
    print(country)
    year_filter = battles[(battles['year'] >= start)
                          & (battles['year'] <= end)]
    attacker_countries = year_filter['attacker'].unique()
    defender_countries = year_filter['defender'].unique()
    countries = set(attacker_countries) | set(defender_countries)
    countries = sorted(countries)
    if country not in countries:
        country = countries[0]
        return [countries, country]
    else:
        return [countries, no_update]


def filter_opponent(value, range_value):
    start, end = range_value
    year_filter = battles[(battles['year'] >= start)
                          & (battles['year'] <= end)]
    usa_battles = year_filter[(year_filter['attacker'] == value)
                              | (year_filter['defender'] == value)]
    countries = usa_battles['attacker'].unique().tolist(
    ) + usa_battles['defender'].unique().tolist()
    countries = set(countries)
    countries.remove(value)
    countries = list(countries)
    return countries


@app.callback(
    [Output('contrincante-dropdown', 'data'),
     Output('contrincante-dropdown', 'disabled'), Output('country-store', 'data'), Output('contrincante-dropdown', 'error'), Output('opponent-list-store', 'data')],
    [Input('country-dropdown', 'value'), Input('range-slider', 'value')],
)
def update_opponent_select(value, range_value):
    countries = filter_opponent(value, range_value)
    return [countries, len(countries) == 0, value, None if len(countries) > 0 else 'No hay contrincantes disponibles', countries]


@app.callback(
    Output('contrincante-dropdown', 'value'),
    [Input('country-dropdown', 'value'), Input('range-slider', 'value')],
    [State('opponent-store', 'data')]
)
def reset_opponent(value, range_value, stored_value,):
    countries = filter_opponent(value, range_value)
    if stored_value in countries:
        return no_update
    else:
        return None


@app.callback(
    Output('opponent-store', 'data'),
    [Input('contrincante-dropdown', 'value')],
)
def update_opponent_state(value):
    return value
