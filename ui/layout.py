from dash import html, dcc
import dash_mantine_components as dmc
import conflicts
from dash_iconify import DashIconify
import map
import deaths
import troops
import opponent
import map_explanation

__years = [{"value": year, "label": year}
           for year in range(1600, 1974, 50)] + [{"value": 1973, "label": 1973}]


def get_layout():
    return dmc.MantineProvider(dmc.Flex([
        html.Div([
            dmc.Title("Batallas militares históricas", order=1),
            dmc.Text(
                "Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.", size="sm"),
        ], className="title-container"),
        dmc.Divider(variant="solid", id="map-divider"),
        dmc.Flex([
            dmc.Flex([
                dcc.Graph(id='historical_map', animate=True, animation_options={
                    'frame': {'redraw': True}}, config={'displayModeBar': False, 'scrollZoom': False}, style={'width': '100%', "height": "650px"}),
                dmc.Divider(orientation="vertical", style={
                            "height": "650px", 'margin-left': 'auto'}),
                dcc.Store(id='map-data', data=None),
                html.Div(id='map-explanation',
                         style={"min-width": '25%', 'width': '25%', 'height': '100%'})
            ], w="100%", gap="lg", h='650px'),
            dmc.Flex([
                dmc.ActionIcon(
                    DashIconify(
                        icon="radix-icons:play", id="button_icon"),
                    size="lg",
                    id="button_toggle"
                ),
                dcc.Store(id='animation_state', data={
                          'state': 'paused', 'current_year': None}),
                dcc.Interval(id='interval-map', interval=1000,
                             n_intervals=0, disabled=True)
            ], justify="center", gap="xs"),
        ], direction="column", gap="lg", pos="relative"),
        dmc.Divider(variant="solid"),
        dmc.Flex(
            [
                dmc.RangeSlider(
                    id="range-slider",
                    marks=__years,
                    max=1973,
                    min=1600,
                    mb=35,
                    minRange=100,
                    labelAlwaysOn=True,
                    value=[1600, 1973]
                ),
                dmc.Flex(
                    [
                        dmc.Select(
                            id='country-dropdown',
                            data=None,
                            searchable=True,
                            value='Alemania',
                            allowDeselect=False,
                            w="100%",
                            label="País",

                        ),
                        dcc.Store(id='country-store', data='Alemania'),
                        dmc.Select(
                            id='contrincante-dropdown',
                            disabled=True,
                            searchable=True,
                            clearable=True,
                            placeholder="Seleccione un contrincante para analizar",
                            w="100%",
                            label="Contrincante",
                        ),
                        dcc.Store(id='opponent-list-store', data=None),
                        dcc.Store(id='opponent-store', data=None),
                    ], direction={"base": "column", "md": "row"}, gap={"base": "xs", "md": "lg"}
                )
            ], direction="column", gap="sm", w="100%"
        ),
        dmc.Flex([
            dmc.Card([
                dmc.CardSection(
                    children=[
                        dmc.Group(
                            children=[
                                dmc.Text(
                                    "Conflictos que involucran a Alemania, entre 1600 y 1973", fw=500, id='graph-title'),
                                dmc.ActionIcon(
                                    DashIconify(
                                        icon="carbon:overflow-menu-horizontal"),
                                    color="gray",
                                    variant="transparent",
                                ),
                            ],
                            justify="space-between",
                        ),
                        dmc.Group(
                            children=[
                                dmc.Text(None, fw=400,
                                         id='graph-subtitle'),
                            ],
                        ),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dcc.Graph(id='graph', config={'displayModeBar': False})
            ], withBorder=True,
                shadow="sm",
                radius="md",
                w="100%"
            ),
            dmc.Card([
                dmc.CardSection(
                    children=[
                        dmc.Group(
                            children=[
                                dmc.Text(
                                    "Resultados de Batallas para Alemania, entre 1600 y 1973", fw=500, id='pie-chart-title'),
                                dmc.ActionIcon(
                                    DashIconify(
                                        icon="carbon:overflow-menu-horizontal"),
                                    color="gray",
                                    variant="transparent",
                                ),
                            ],
                            justify="space-between",
                        ),
                        dmc.Group(
                            children=[
                                dmc.Text(None, fw=400,
                                         id='pie-chart-subtitle'),
                            ],
                        ),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dcc.Graph(
                    id='pie-chart', config={'displayModeBar': False}, style={'marginTop': 'auto', 'marginBottom': 'auto'})
            ], withBorder=True,
                shadow="sm",
                radius="md",
                w="100%",
            ),
        ], direction={"base": "column", "md": "row"}, w="100%", gap="lg", justify="space-between"),
        dmc.Flex([
            dmc.Card([
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text(
                                "Distribución de las muertes en batalla que involucran a Alemania, entre 1600 y 1973", fw=500, id='boxplot-deaths-title'),
                            dmc.ActionIcon(
                                DashIconify(
                                    icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        justify="space-between",
                    ),
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dcc.Graph(id='boxplot_deaths', config={
                          'displayModeBar': False})
            ], withBorder=True,
                shadow="sm",
                radius="md",
                w="100%"
            ),
            dmc.Card([
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text(
                                "Proporción de tropas en batallas que involucran a Alemania, entre 1600 y 1973", fw=500, id='battle-troops-title'),
                            dmc.ActionIcon(
                                DashIconify(
                                    icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        justify="space-between",
                    ),
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dcc.Graph(id='battle-troops', config={'displayModeBar': False})
            ], withBorder=True,
                shadow="sm",
                radius="md",
                w="100%"
            ),
        ], direction={"base": "column", "md": "row"}, w="100%", gap="lg", justify="space-between")
    ], gap="lg", direction="column"))
