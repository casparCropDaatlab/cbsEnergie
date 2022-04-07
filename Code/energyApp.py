from turtle import width
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback

import plotly
import plotly_express as px
import plotly.graph_objects as go

import pandas
import cbsodata

from pages import page1, page2

## Get the CBS energy data
dfCbsEnergy = pandas.DataFrame(cbsodata.get_data('83140NED'))

# print(list(dfCbsEnergy.columns.values()))
# print(list(dfCbsEnergy['Energiedragers'].unique()))

## Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ]
)

## App layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.NavbarSimple(
                children=[
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Energieaanbod tijdlijn", href="/page1", className="text-black"),
                            dbc.DropdownMenuItem("Energieaanbod per jaar", href="/page2", className="text-black"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Energieaanbod",
                        toggleClassName="text-white"
                    ),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Totaal verbruik tijdlijn", href="/page3", className="text-white"),
                            dbc.DropdownMenuItem("Totaal verbruik per jaar", href="/page4", className="text-black"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Energieverbruik",
                        toggleClassName="text-white"
                    ),
                ],
                brand="Dashboard energie in nederland",
                brand_href="/",
                color="primary",
                className="text-center mt-2 mb-2 text-white",
                brand_style={'color':'white'}
            )
        ], width=10, className="offset-1")
    ], className="bg-primary"),
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return page1.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return '404'

## Run the Dash app
app.run_server(port='8002')