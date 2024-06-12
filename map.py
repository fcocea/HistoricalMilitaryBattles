import plotly.express as px
from dash_manager import app
from dash import Output, Input

@app.callback(
    [Output("historical_map", "figure")],
    [Input("range-slider-callback", "value")]
)


def get_map(selected_years):
    historical_map = px.choropleth()

    return [historical_map]