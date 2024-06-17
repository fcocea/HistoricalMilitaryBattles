from dash_manager import app
from dash import Output, Input, State
import pandas as pd

battles = pd.read_csv('data/battles_clean.csv')


@app.callback(
    [Output('contrincante-dropdown', 'data'),
     Output('contrincante-dropdown', 'disabled')],
    [Input('country-dropdown', 'value')],
)
def update_opponent_select(value):
    usa_battles = battles[(battles['attacker'] == value)
                          | (battles['defender'] == value)]
    countries = usa_battles['attacker'].unique().tolist(
    ) + usa_battles['defender'].unique().tolist()
    countries = set(countries)
    countries.remove(value)
    countries = list(countries)
    return [countries, False]


@app.callback(
    Output('contrincante-dropdown', 'value'),
    [Input('country-dropdown', 'value')]
)
def reset_opponent(value):
    return None
