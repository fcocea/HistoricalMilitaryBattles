import plotly.express as px
from dash_manager import app
from dash import Output, Input

@app.callback(
    [Output("historical_map", "figure")],
    [Input("range-slider-callback", "value")]
)


def get_map(selected_years):
    historical_map = px.choropleth()
    historical_map.update_geos(projection_type="natural earth")
    historical_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return [historical_map]