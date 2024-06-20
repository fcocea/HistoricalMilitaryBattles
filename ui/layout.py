from dash import html, dcc
import dash_mantine_components as dmc
from conflicts import countries
from dash_iconify import DashIconify
import map
import deaths
import troops
import opponent

__years = [{"value": year, "label": year}
           for year in range(1600, 1974, 50)] + [{"value": 1973, "label": 1973}]


def get_layout():
    return dmc.MantineProvider(dmc.Flex([
        html.Div([
            dmc.Title("Batallas militares históricas", order=1),
            dmc.Text(
                "Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.", size="sm"),
            html.Img(src="assets/soldadito.png",
                     width=100, height=150, id="soldier", className='soldier hidden')
        ], className="title-container"),
        dmc.Divider(variant="solid", id="map-divider"),
        dmc.Flex([
            html.Img(src="assets/explosion.gif", width=200, height=200, id="bomb-1", style={
                'position': 'absolute', 'top': '0', 'z-index': '100'}, className="hidden"
            ),
            html.Img(src="assets/explosion.gif", width=200, height=200, id="bomb-2", style={
                'position': 'absolute', 'top': '0', "right": '0', 'z-index': '100'}, className="hidden"
            ),
            dcc.Graph(id='historical_map', animate=True, animation_options={
                      'frame': {'redraw': True}}, config={'displayModeBar': False}, ),
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
                    id="range-slider-callback",
                    marks=__years,
                    max=1973,
                    min=1600,
                    mb=35,
                    minRange=25,
                    labelAlwaysOn=True,
                    value=[1600, 1973]
                ),
                dmc.Flex(
                    [
                        dmc.Select(
                            id='country-dropdown',
                            data=countries,
                            searchable=True,
                            value='Alemania',
                            allowDeselect=False,
                            w="100%",
                            label="País",

                        ),
                        dmc.Select(
                            id='contrincante-dropdown',
                            disabled=True,
                            searchable=True,
                            clearable=True,
                            placeholder="Seleccione un contrincante para analizar",
                            w="100%",
                            label="Contrincante"
                        ),
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
                                    "Conflictos que involucran a Alemania", fw=500, id='graph-title'),
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
                                dmc.Text("Subtitulo",fw=400, id='graph-subtitle'),
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
                                    "Conflictos que involucran a Alemania", fw=500, id='pie-chart-title'),
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
                                dmc.Text("Subtitulo pie chart",fw=400, id='pie-chart-subtitle'),
                            ],
                        ),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dcc.Graph(id='pie-chart', config={'displayModeBar': False})
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
                                "Distribución de las muertes en batalla que involucran a Alemania", fw=500, id='boxplot-deaths-title'),
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
                                "Waffle Chart de Alemania", fw=500, id='battle-troops-title'),
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
