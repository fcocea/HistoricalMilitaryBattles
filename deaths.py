import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash_manager import app
from dash import Output, Input

battles = pd.read_csv('data/battles_clean.csv')
df_belligerents = pd.read_csv('data/belligerents.csv')

battles['year'] = battles['date_start'].str.extract(r'(\d{4})')
battles['year'] = battles['year'].astype(int)


@app.callback(
    [Output('boxplot_deaths', 'figure'), Output(
        'boxplot-deaths-title', 'children')],
    [Input('country-dropdown', 'value'),
     Input('contrincante-dropdown', 'value'), Input('range-slider', 'value')]
)
def boxplot_deaths(selected_country, selected_contrincante=None, range_value=[1600, 1973]):
    start, end = range_value
    year_filter = battles[(battles['year'] >= start)
                          & (battles['year'] <= end)]
    if selected_contrincante is None:
        deaths = year_filter[(year_filter['attacker'] == selected_country) | (
            year_filter['defender'] == selected_country)]
        deaths = deaths[['isqno', 'attacker', 'defender', 'date_start']]
        deaths['date_start'] = pd.to_datetime(deaths['date_start'])
        deaths = deaths.merge(df_belligerents, on='isqno')
        deaths['country'] = np.where(
            deaths['attacker_y'] == 1, deaths['attacker_x'], deaths['defender'])
        deaths.drop(columns=['attacker_x', 'attacker_y',
                    'defender', 'actors'], inplace=True)
        deaths = deaths[deaths['country'] == selected_country]
        deaths = deaths.dropna(subset=['cas'])
        deaths = deaths[['isqno', 'cas', 'country']]
        deaths = deaths.rename(columns={'cas': selected_country})
        deaths = deaths.drop(columns=['country'])
        deaths = deaths.set_index('isqno')

        fig = px.box(deaths, orientation='h')
        # color #3399FF
        fig.update_traces(marker_color='#3399FF')
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        fig.update_xaxes(showgrid=False, showline=False)
        fig.update_yaxes(showgrid=False, showline=False)

        fig.update_yaxes(title_text='País')
        fig.update_xaxes(title_text='Muertes en batalla')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        return [fig, f"Distribución de las muertes en batallas que involucran a {selected_country}, entre {start} y {end}"]
    else:
        # Filtra para obtener batallas donde ambos países están involucrados
        deaths = year_filter[((year_filter['attacker'] == selected_country) & (year_filter['defender'] == selected_contrincante)) |
                             ((year_filter['attacker'] == selected_contrincante) & (year_filter['defender'] == selected_country))]
        deaths = deaths[['isqno', 'attacker', 'defender', 'date_start']]
        deaths['date_start'] = pd.to_datetime(deaths['date_start'])
        deaths = deaths.merge(df_belligerents, on='isqno')

        deaths['country'] = np.where(
            deaths['attacker_y'] == 1, deaths['attacker_x'], deaths['defender'])
        deaths.drop(['attacker_x', 'defender', 'attacker_y'],
                    axis=1, inplace=True)
        deaths = deaths[['isqno', 'country', 'date_start', 'cas']]

        deaths_attacker = deaths[deaths['country'] == selected_country].copy()
        deaths_attacker.rename(columns={'cas': selected_country}, inplace=True)
        deaths_attacker.drop('country', axis=1, inplace=True)
        # borrar date_start
        deaths_attacker.drop('date_start', axis=1, inplace=True)
        deaths_defender = deaths[deaths['country']
                                 == selected_contrincante].copy()
        deaths_defender.rename(
            columns={'cas': selected_contrincante}, inplace=True)
        deaths_defender.drop('country', axis=1, inplace=True)
        deaths_defender.drop('date_start', axis=1, inplace=True)

        deaths_attacker = deaths_attacker.merge(deaths_defender, on='isqno')
        deaths_attacker.set_index('isqno', inplace=True)
        deaths_attacker_melted = deaths_attacker.reset_index().melt(
            id_vars=['isqno'], var_name='country', value_name='casualties')

        fig = px.box(
            deaths_attacker_melted,
            x='casualties',
            color='country',  # Indica la columna que define los colores
            orientation='h',  # Orientación horizontal
            color_discrete_map={
                selected_country: '#3399FF',  # Azul para Independentistas
                selected_contrincante: '#DC143C'              # Rojo para España
            },
            category_orders={"country": [
                selected_country, selected_contrincante]}
        )
        fig.update_layout(
            showlegend=False,  # Ocultar la leyenda
            plot_bgcolor='white',  # Fondo blanco para el gráfico
            yaxis=dict(
                title='',  # Remover el título del eje Y
                showgrid=True,  # Mostrar la rejilla
                tickmode='array',
                tickvals=[-0.17, 0.17],  # Posiciones de las etiquetas
                # Texto de las etiquetas
                ticktext=[selected_country, selected_contrincante]
            )
        )
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        fig.update_layout(yaxis_title="Países",
                          xaxis_title="Muertes en batalla")

        return [fig, f"Distribución de las muertes en batallas de {selected_country} contra {selected_contrincante}, entre {start} y {end}"]
