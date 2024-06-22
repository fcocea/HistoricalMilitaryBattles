from shapely.ops import orient
import geopandas as gpd
import json
import plotly.express as px
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


# # Load the data
# gdf = gpd.read_file('data/geo/concat_simply.geojson')
# gdf = gdf[['name', 'geometry']]
# df = df[['isqno', 'locn', 'date_start']]

# # Merge gdf by name and df by locn
# gdf = gdf.rename(columns={'name': 'locn'})
# gdf['locn'] = gdf['locn'].str.lower()
# df['locn'] = df['locn'].str.lower()

# gdf = gdf.merge(df, on='locn')

# # Convert date_start to year
# gdf = gdf.drop(columns=['date_start'])

# # Group by location and year, count isqno, and keep the geometry
# gdf = gdf.groupby(['locn', 'year']).agg(
#     {'isqno': 'count', 'geometry': 'first'}).reset_index()
# gdf = gdf.rename(columns={'isqno': 'count'})

# gdf = gdf.sort_values(by=['year'])
# gdf['geometry'] = gdf['geometry'].apply(orient, args=(-1,))
# geojson = gdf.set_geometry('geometry').__geo_interface__


gdf = gpd.read_file('data/geo/geoPoints.geojson')
gdf = gdf.rename(columns={'name': 'locn'})
gdf['locn'] = gdf['locn'].str.lower()
df['locn'] = df['locn'].str.lower()
gdf = gdf.merge(df, on='locn')
gdf['date_start'] = pd.to_datetime(gdf['date_start'])
gdf['year'] = gdf['date_start'].dt.year
gdf['lon'] = gdf['geometry'].apply(lambda x: x.x)
gdf['lat'] = gdf['geometry'].apply(lambda x: x.y)
gdf = gdf.groupby(['locn', 'year']).agg(
    {'isqno': 'count', 'lon': 'first', 'lat': 'first'}).reset_index()
gdf = gdf.rename(columns={'isqno': 'count'})


@app.callback(
    [Output("historical_map", "figure"), Output("map-divider", "label")],
    [Input("animation_state", "data")]
)
def get_map(state):
    current_year = state['current_year']
    # df_year = gdf
    df_year = gdf[gdf['year'] ==
                  current_year] if current_year is not None else df[df['Year'] == _years[0]]
    fig = go.Figure(go.Scattermapbox(
        lat=df_year['lat'],
        lon=df_year['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='gray',
            symbol="marker",
            allowoverlap=True
        ),
    ))

    fig.update_layout(
        dragmode=False,
        mapbox=dict(
            accesstoken="pk.eyJ1IjoiZmNvY2VhIiwiYSI6ImNsZ250dzh0bTA2MHkzZ3FtNzhvbGptdmoifQ.BOpVSmp0vR-SovUo7Q_NAw",
            zoom=1.3,
            center=dict(lat=22, lon=16),
        ),
        showlegend=False
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return [fig, f"Año {current_year}" if current_year is not None else None]


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
