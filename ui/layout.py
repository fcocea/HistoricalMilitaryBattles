from dash import html, dcc, Output, Input
import dash_mantine_components as dmc
from dash_manager import app
from conflicts import countries
from map import get_map

__years = [{"value": year, "label": year} for year in range(1600, 1974, 50)] + [{"value": 1973, "label": 1973}]

def get_layout():
    return dmc.MantineProvider(html.Div([
    html.Div([
        dmc.Title("Batallas militares históricas", order=1),
        dmc.Text("Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.", size="sm"),
    ], className="title-container"),

    html.Div([
        dcc.Graph(id='historical_map')
    ], className="map-container"),

    html.Div(
    [
       dmc.RangeSlider(
            id="range-slider-callback",
            marks=__years,
            max=1973,
            min=1600,
            mb=35,
            minRange=25,
            labelAlwaysOn=True,
            value=[1600,1973]
        ),
        dmc.Space(h=10),
        dmc.Text(id="range-slider-output"), 
    ]
    ),
        dmc.Select(
        id='country-dropdown',
        data=countries,
        searchable=True,
        value='USA',
        allowDeselect=False,
    ),
    dmc.Flex([
        dcc.Graph(id='graph'),
        dcc.Graph(id='pie-chart')
    ], direction={"base": "column", "sm": "row"}, w={"base": "100%", "sm": "100%"}, gap="lg")
]))


@app.callback(
    Output("range-slider-output", "children"), Input("range-slider-callback", "value")
)
def update_value(value):
    return f"You have selected: [{value[0]}, {value[1]}]"

