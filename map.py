import plotly.express as px
from dash_manager import app
from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate


df = pd.read_csv('data/battles_clean.csv')
_years = df['date_start']
_years = _years.apply(lambda x: int(x.split('-')[0]))
_years = _years.unique().tolist()


@app.callback(
    [Output("historical_map", "figure"), Output("map-divider", "label")],
    [Input("animation_state", "data")]
)
def get_map(state):
    current_year = state['current_year']
    # df_year = df[df['Year'] ==
    #              current_year] if current_year is not None else df[df['Year'] == _years[0]]
    historical_map = px.choropleth()
    historical_map.update_geos(projection_type="natural earth")
    historical_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    historical_map.update_layout(dragmode=False)

    return [historical_map, f"Año {current_year}" if current_year is not None else None]


@app.callback(
    [Output('button_icon', 'icon'),
     Output('animation_state', 'data', allow_duplicate=True), Output('interval-map', 'disabled')],
    [Input('button_toggle', 'n_clicks'), State('animation_state', 'data')],
    prevent_initial_call=True
)
def toggle_play_pause(n_clicks, current_state):
    return ["radix-icons:play" if current_state['state'] == 'playing' else "radix-icons:pause", {
        'state': 'paused' if current_state['state'] == 'playing' else 'playing',
        'current_year': current_state['current_year']
    }, True if current_state['state'] == 'playing' else False]


@app.callback(
    Output('animation_state', 'data'),
    [Input('interval-map', 'n_intervals')],
    [State('animation_state', 'data')],
    prevent_initial_call=False
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
        if animation_state['current_year'] is None:
            return {'state': 'paused', 'current_year': _years[0]}
        raise PreventUpdate
