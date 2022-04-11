## Import dependency packages
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

## Get the CBS energy data
dfCbsEnergy = pandas.DataFrame(cbsodata.get_data('83140NED'))

##Set categories for totals
totalEnergyCategories = [
    'Totaal kool en koolproducten',
    'Totaal aardoliegrondstoffen en producten',
    'Aardgas',
    'Hernieuwbare energie',
    'Elektriciteit',
    'Warmte',
    'Kernenergie'
]

#"Totaal verbruik tijdlijn"

## Prepare DataFrame for and build the graph of total energy sources over years
energyUseTotalTimelineDf = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
energyUseTotalTimelineFig = px.line(
    x=energyUseTotalTimelineDf['Perioden'],
    y=energyUseTotalTimelineDf['TotaalEnergieverbruik_9'],
    color=energyUseTotalTimelineDf['Energiedragers'],
    labels={"y": "Totaalverbruik", "x":"Jaren", "color":"Energiedragers"},
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

## Set the layout for page 3
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Energie verbruik over de jaren", className="text-center pb-2 text-white"),
            dcc.Graph(
                id='energie-verbruik-per-drager-timeline',
                figure=energyUseTotalTimelineFig
            )
        ], width=10, className="offset-1 bg-secondary pb-1")
    ], className="mb-5 mt-5 bg-secondary pt-3 pb-5"),
])