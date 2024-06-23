import geopandas as gpd
from dash_manager import app
from dash import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

df = pd.read_csv('data/battles_clean.csv')

_years = df['date_start']
_years = _years.apply(lambda x: int(x.split('-')[0]))
_years = _years.unique().tolist()
_years.sort()

gdf = gpd.read_file('data/geo/geoPoints.geojson')
gdf = gdf.rename(columns={'name': 'locn'})
gdf['locn'] = gdf['locn'].str.title()
df['locn'] = df['locn'].str.title()
gdf = gdf.merge(df, on='locn')
gdf['date_start'] = pd.to_datetime(gdf['date_start'])
gdf['year'] = gdf['date_start'].dt.year
gdf['lon'] = gdf['geometry'].apply(lambda x: x.x)
gdf['lat'] = gdf['geometry'].apply(lambda x: x.y)

gdf['war'] = gdf['war'].apply(lambda x: x.title().replace("'S", "'s"))
gdf['name'] = gdf['name'].apply(lambda x: x.title())

gdf = gdf.groupby(['locn', 'year']).agg(
    {'isqno': 'count', 'lon': 'first', 'lat': 'first', 'name': list, 'war': list, 'winner': list, 'attacker': list, 'defender': list}).reset_index()
gdf = gdf.rename(columns={'isqno': 'count'})
gdf['attacker_defender'] = gdf['attacker'].str[0] + \
    ' vs ' + gdf['defender'].str[0]
# apply title to war and name


def get_battles(row):
    battles = {}
    for i in range(len(row['name'])):
        if row['war'][i] not in battles:
            battles[row['war'][i]] = []
        battles[row['war'][i]].append({
            'name': row['name'][i],
            'winner': 'Empate' if row['winner'] == 'draw' else row['attacker'][i] if row['winner'][i] == 'attacker' else row['defender'][i],
            'attacker': row['attacker'][i],
            'defender': row['defender'][i],
            'location': row['locn'].title()
        })
    return battles


gdf['data'] = gdf.apply(get_battles, axis=1)
gdf = gdf.drop(columns=['war', 'name', 'winner', 'attacker', 'defender'])
gdf


@app.callback(
    [Output("historical_map", "figure"), Output(
        "map-divider", "label"), Output('map-data', 'data')],
    [Input("animation_state", "data")],
)
def get_map(state):
    current_year = state['current_year']
    df_year = gdf[gdf['year'] ==
                  current_year] if current_year is not None else df[df['Year'] == _years[0]]
    fig = go.Figure(go.Scattermapbox(
        lat=df_year['lat'],
        lon=df_year['lon'],
        mode='markers',
        hoverinfo='text',
        hovertext=df_year['attacker_defender'] + '<br>' +
        'Lugar: ' + df_year['locn'].astype(str) + '<br >' +
        'Número de batallas: ' + df_year['count'].astype(str),
        marker=go.scattermapbox.Marker(
            size=10,  # df_year['count'],
            color='white',
            symbol="marker",
            allowoverlap=True,
        ),
    ))

    fig.update_layout(
        dragmode=False,
        mapbox=dict(
            accesstoken="pk.eyJ1IjoiZmNvY2VhIiwiYSI6ImNsZ250dzh0bTA2MHkzZ3FtNzhvbGptdmoifQ.BOpVSmp0vR-SovUo7Q_NAw",
            zoom=1.3,
            center=dict(lat=22, lon=16),
        ),
        showlegend=False,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return [fig, f"Año {current_year}" if current_year is not None else None, {
        'year': current_year,
        'battles': df_year['data'].to_list()
    }]


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
    }, True if current_state['state'] == 'playing' else False
    ]


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
