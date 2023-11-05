from dash.dependencies import Output, Input
from flask import Flask
from app_get_data import get_data_for_dashboard
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Dashboard'

df_weather, df_air_quality = get_data_for_dashboard.get_data_postgres()

# Define the app layout
app.layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2("Dashboard Data"), width={'size': 12, 'offset': 0, 'order': 0}), style = {'textAlign': 'center', 'paddingBottom': '1%'}),


    dbc.Tabs([
        dbc.Tab(label="Air Quality", children=[

            dbc.Row(dbc.Col(html.Div([
                    # Dropdown for selecting v_name
                    dcc.Dropdown(
                        id='id-dropdown',
                        options=[{'label': str(id), 'value': id} for id in df_air_quality['v_name'].unique()],
                        value=df_air_quality['v_name'].unique()[0],  # Default to the first unique ID
                        style={'width': '200px'} # Set the width of the dropdown
                    )
                ])
                )
            ),

            dbc.Row(dbc.Col(html.Div([

                # Line chart for n_pm10
                html.Div([
                    dcc.Graph(id='line-chart-pm10')
                ], style={'display': 'inline-block','width': '50%'}),
                # Line chart for n_pm2_5
                html.Div([
                    dcc.Graph(id='line-chart-pm2_5')
                ], style={'display': 'inline-block','width': '50%'}),

            ])
            )
            ),
        ]),

        dbc.Tab(label="Weather", children=[

            dbc.Row(dbc.Col(html.Div([
                    # Dropdown for selecting v_name
                    dcc.Dropdown(
                        id='weather-id-dropdown',
                        options=[{'label': str(id), 'value': id} for id in df_weather['v_name'].unique()],
                        value=df_weather['v_name'].unique()[0],  # Default to the first unique ID
                        style={'width': '200px'} # Set the width of the dropdown
                    )
                ])
                )
            ),

            dbc.Row(dbc.Col(html.Div([

                # Line chart for temperature
                html.Div([
                    dcc.Graph(id='weather-line-chart-temperature')
                ], style={'display': 'inline-block','width': '50%'}),
                # Line chart for visibility
                html.Div([
                    dcc.Graph(id='weather-line-chart-visibility')
                ], style={'display': 'inline-block','width': '50%'}),

            ])
            )
            ),

            dbc.Row(dbc.Col(html.Div([

                # Line chart for temperature
                html.Div([
                    dcc.Graph(id='weather-line-chart-relativehumidity_2m')
                ], style={'display': 'inline-block','width': '50%'}),
                # Line chart for visibility
                html.Div([
                    dcc.Graph(id='weather-line-chart-uv-index')
                ], style={'display': 'inline-block','width': '50%'}),

            ])
            )
            ),


        ]),
    ]),

])
    

@app.callback(
    [Output('line-chart-pm10', 'figure'), Output('line-chart-pm2_5', 'figure')],
    Input('id-dropdown', 'value'))

def update_line_chart(selected_id):
    filtered_data = df_air_quality[df_air_quality['v_name'] == selected_id]

    fig_pm10 = px.line(
        filtered_data, x='d_date', y='n_pm10',
        title=f'n_pm10 for ID: {selected_id}',
        labels={'n_pm10': 'PM10 Levels', 'd_date': 'Date'},
    )

    fig_pm2_5 = px.line(
        filtered_data, x='d_date', y='n_pm2_5',
        title=f'n_pm2_5 for ID: {selected_id}',
        labels={'n_pm2_5': 'PM2.5 Levels', 'd_date': 'Date'},
    )

    return fig_pm10, fig_pm2_5

@app.callback(
    [Output('weather-line-chart-temperature', 'figure'), Output('weather-line-chart-visibility', 'figure'), Output('weather-line-chart-relativehumidity_2m', 'figure'), Output('weather-line-chart-uv-index', 'figure')],
    Input('weather-id-dropdown', 'value')
)
def update_weather_line_charts(selected_id):
    filtered_data = df_weather[df_weather['v_name'] == selected_id]

    fig_temperature = px.line(
        filtered_data, x='d_date', y='n_temperature_2m',
        title=f'Temperature for ID: {selected_id}',
        labels={'n_temperature_2m': 'Temperature', 'd_date': 'Date'},
    )

    fig_visibility = px.line(
        filtered_data, x='d_date', y='n_visibility',
        title=f'Visibility for ID: {selected_id}',
        labels={'n_visibility': 'Visibility', 'd_date': 'Date'},
    )

    fig_relativehumidity_2m = px.line(
        filtered_data, x='d_date', y='n_relativehumidity_2m',
        title=f'Visibility for ID: {selected_id}',
        labels={'n_relativehumidity_2m': 'Relative Humidity', 'd_date': 'Date'},
    )

    fig_uv_index = px.line(
        filtered_data, x='d_date', y='n_uv_index',
        title=f'Visibility for ID: {selected_id}',
        labels={'n_uv_index': 'Uv Index', 'd_date': 'Date'},
    )

    return fig_temperature, fig_visibility, fig_relativehumidity_2m, fig_uv_index


if __name__=='__main__':
    app.run_server(debug=True)