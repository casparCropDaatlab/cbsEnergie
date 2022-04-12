## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy, totalEnergyCategories

## Prepare DataFrame for and the graph of total energy sources over years
energySrcsTotalTimelnDf = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]

## Build the figure for the "Energie aanbod" timeline graph
energySourcesTotalOverTimeFigure = px.line(
    x=energySrcsTotalTimelnDf['Perioden'], y=energySrcsTotalTimelnDf['TotaalAanbodTPES_1'],
    color=energySrcsTotalTimelnDf['Energiedragers'],
    color_discrete_map={
        "Totaal kool en koolproducten": "brown", "Totaal aardoliegrondstoffen": "black",
        "Totaal aardolieproducten": "purple", "Aardgas": "blue", "Hernieuwbare energie": "green",
        "Elektriciteit": "magenta", "Warmte": "red", "Kernenergie": "goldenrod"
    },
    labels={"y": "Totaalaanbod (TPES)", "x":"Jaren", "color":"Energiedragers"},
    height=600, markers=True
)

## Update graph layout for correct visualisation
energySourcesTotalOverTimeFigure.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1
    )
)

## Set the layout for page 1 "Energy Sources timeline"
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Energie aanbod in TPES over de jaren",
                        className="text-center pb-2 text-white"
                    ),
                    dcc.Graph(
                        id='energie-aanbod-per-drager-timeline', figure=energySourcesTotalOverTimeFigure
                    )
                ], width=10, className="offset-1 bg-secondary pb-1"
            )
        ], className="mb-5 mt-5 bg-secondary pt-3 pb-5"
    ),
])