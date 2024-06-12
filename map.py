import plotly.express as px
from dash_manager import app
from dash import dcc, Output, Input, State
import pandas as pd


df = pd.read_csv('https://gist.githubusercontent.com/shinokada/f01139d3a024de375ede23cec5d52360/raw/424ac0055ed71a04e6f45badfaef73df96ad0aad/CrimeStatebyState_1960-2014.csv')
df = df[(df['State'] != 'District of Columbia')]

_years = df['Year'].unique()
_years.sort()
_years = _years.tolist()


@app.callback(
    [Output("historical_map", "figure"), Output("map-divider", "label")],
    [Input("animation_state", "data")]
)
def get_map(state):
    current_year = state['current_year']
    df_year = df[df['Year'] ==
                 current_year] if current_year is not None else df[df['Year'] == _years[0]]
    map_fig = px.choropleth(df_year,
                            locations='State_code',
                            color="Murder_per100000",
                            color_continuous_scale="Inferno",
                            locationmode='USA-states',
                            scope="usa",
                            range_color=(0, 20),
                            title='Crime by State',
                            height=600,
                            )
    return [map_fig, f"Año {current_year}"]


app.clientside_callback(
    """
    function(n_clicks, current_state) {
        var graphDiv = document.querySelector('#historical_map').children[1];
        var new_state = current_state.state === 'paused' ? 'playing' : 'paused';

        if (new_state === 'playing') {
            return ["radix-icons:pause", {
                'state': new_state,
                'current_year': current_state['current_year']
            }];
        } else {

            return ["radix-icons:play", {
                'state': new_state,
                'current_year': current_state['current_year']
            }];
        }
    }
    """,
    [Output('button_icon', 'icon'),
     Output('animation_state', 'data')],
    [Input('button_toggle', 'n_clicks'), State('animation_state', 'data')],
    prevent_initial_call=True
)


@app.callback(
    Output('animation_state', 'data', allow_duplicate=True),
    [Input('interval', 'n_intervals')],
    [State('animation_state', 'data')],
    prevent_initial_call=True
)
def update_current_year(n_intervals, animation_state):
    if animation_state['state'] == 'playing':
        current_year = animation_state['current_year']
        if current_year is None or current_year == _years[-1]:
            current_year = _years[0]
        else:
            current_year = _years[_years.index(current_year) + 1]
        return {'state': 'playing', 'current_year': current_year}
    else:
        return animation_state
