from dash import html, dcc, Output, Input
import dash_mantine_components as dmc
from dash_manager import app
from conflicts import countries
from map import get_map
from dash_iconify import DashIconify

__years = [{"value": year, "label": year}
           for year in range(1600, 1974, 50)] + [{"value": 1973, "label": 1973}]


def get_layout():
    return dmc.MantineProvider(dmc.Flex([
        html.Div([
            dmc.Title("Batallas militares históricas", order=1),
            dmc.Text(
                "Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.", size="sm"),
        ], className="title-container"),
        dmc.Divider(variant="solid", label="Año 1960", id="map-divider"),
        dmc.Flex([
            dcc.Graph(id='historical_map', animate=True, animation_options={
                      'frame': {'redraw': True}}, config={'displayModeBar': False}, ),
            dmc.Flex([
                dmc.Button(
                    DashIconify(width=24,
                                icon="radix-icons:play", id="button_icon"),
                    size="xs",
                    id="button_toggle"
                ),
                dcc.Store(id='animation_state', data={
                          'state': 'paused', 'current_year': 1960}),
                dcc.Interval(id='interval', interval=1000, n_intervals=0)
            ], justify="center", gap="xs"),
        ], direction="column", gap="lg"),
        dmc.Divider(variant="solid"),
        dmc.Flex(
            [
                dmc.RangeSlider(
                    id="range-slider-callback",
                    marks=__years,
                    max=1973,
                    min=1600,
                    mb=35,
                    minRange=25,
                    labelAlwaysOn=True,
                    value=[1600, 1973]
                ),
                dmc.Select(
                    id='country-dropdown',
                    data=countries,
                    searchable=True,
                    value='USA',
                    allowDeselect=False,
                ),
            ], direction="column", gap="sm",
        ),
        dmc.Flex([
            dcc.Graph(id='graph'),
            dcc.Graph(id='pie-chart')
        ], direction={"base": "column", "sm": "row"}, w="100%", gap="lg", justify="space-between"),
    ], gap="lg", direction="column"))
