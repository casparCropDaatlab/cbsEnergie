from turtle import width
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import plotly
import plotly_express as px
import plotly.graph_objects as go

import pandas
from energyApp import dfCbsEnergy

# print(list(dfCbsEnergy.columns.values()))
# print(list(dfCbsEnergy['Energiedragers'].unique()))

## Categories for the total of energy sources
totalEnergyCategories = [
    'Totaal kool en koolproducten',
    'Totaal aardoliegrondstoffen en producten',
    'Aardgas',
    'Hernieuwbare energie',
    'Elektriciteit',
    'Warmte',
    'Kernenergie'
]

## Prepare DataFrame for and build the graph of total energy sources over years
energySourcesTotalOverTimeDF = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
energySourcesTotalOverTimeFigure = px.line(
    x=energySourcesTotalOverTimeDF['Perioden'],
    y=energySourcesTotalOverTimeDF['TotaalAanbodTPES_1'],
    color=energySourcesTotalOverTimeDF['Energiedragers'],
    labels={"y": "Totaalaanbod (TPES)", "x":"Jaren", "color":"Energiedragers"},
    color_discrete_map={
        "Totaal kool en koolproducten": "brown",
        "Totaal aardoliegrondstoffen en producten": "black",
        "Aardgas": "blue",
        "Hernieuwbare energie": "green",
        "Elektriciteit": "magenta",
        "Warmte": "red",
        "Kernenergie": "goldenrod"
    },
    height=600,
    markers=True
)

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Energie aanbod in TPES over de jaren", className="text-center pb-2 text-white"),
            dcc.Graph(
                id='energie-aanbod-per-drager-timeline',
                figure=energySourcesTotalOverTimeFigure
            )
        ], width=10, className="offset-1 bg-secondary pb-1")
    ], className="mb-5 mt-5 bg-secondary pt-3 pb-5"),
])