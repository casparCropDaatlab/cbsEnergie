## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy, totalEnergyCategories

## Prepare DataFrame for total energy use over years
energyUseTotalTimelineDf = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]

## Build the graph of total energy use over years
energyUseTotalTimelineFig = px.line(
    x=energyUseTotalTimelineDf['Perioden'], y=energyUseTotalTimelineDf['TotaalEnergieverbruik_9'],
    color=energyUseTotalTimelineDf['Energiedragers'],
    color_discrete_map={
        "Totaal kool en koolproducten": "brown", "Totaal aardoliegrondstoffen": "black",
        "Totaal aardolieproducten": "purple", "Aardgas": "blue", "Hernieuwbare energie": "green",
        "Elektriciteit": "magenta", "Warmte": "red", "Kernenergie": "goldenrod"
    },
    labels={"y": "Totaalverbruik", "x":"Jaren", "color":"Energiedragers"}, height=600, markers=True
)

## Update graph layout for correct visualisation
energyUseTotalTimelineFig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1
    )
)

## Set the layout for page 3
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Energie verbruik over de jaren",
                        className="text-center pb-2 text-white"
                    ),
                    dcc.Graph(
                        id='energie-verbruik-per-drager-timeline', figure=energyUseTotalTimelineFig
                    )
                ], width=10, className="offset-1 bg-secondary pb-1"
            )
        ], className="mb-5 mt-5 bg-secondary pt-3 pb-5"
    )
])