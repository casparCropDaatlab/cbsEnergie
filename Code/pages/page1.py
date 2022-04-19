## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy
from energyAppGlobalData import totalEnergyCategoriesWhole as totalEnergyCategories

## Prepare DataFrame for and the graph of total energy sources over years
energySrcsTotalTimelnDf = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]

## Build the figure for the "Energie aanbod" timeline graph
energySourcesTotalOverTimeFigure = px.line(
    x=energySrcsTotalTimelnDf['Perioden'], y=energySrcsTotalTimelnDf['TotaalAanbodTPES_1'],
    color=energySrcsTotalTimelnDf['Energiedragers'],
    color_discrete_map={
        "Totaal kool en koolproducten": "brown", "Elektriciteit": "magenta", "Warmte": "red",
        "Totaal aardoliegrondstoffen en producten": "black",
        "Aardgas": "blue", "Hernieuwbare energie": "green", "Kernenergie": "#FAE500"
    },
    labels={"y": "Totaalaanbod (TPES)", "x":"Jaren", "color":"Energiedragers"},
    height=550, markers=True
)

## Update graph layout for correct visualisation
energySourcesTotalOverTimeFigure.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1,
        xanchor="right", x=1
    ),
    plot_bgcolor= 'rgba(192,192,192,0.75)',
    paper_bgcolor= 'rgba(0,0,0,0)',
    font= dict(color="white")
)

## Set the layout for page 1 "Energy Sources timeline"
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3(
                        "Energie aanbod in TPES over de jaren", className="text-center text-white"
                    ),
                    dcc.Graph(
                        id='energie-aanbod-per-drager-timeline', figure=energySourcesTotalOverTimeFigure
                    )
                ],  xs= 12, sm= 12, md= 12, lg= 9, xl= 9, xxl= 9, className="mb-2 mt-2 p-2"
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader([
                                html.H5("Uitleg bij deze grafiek:")
                            ]),
                            dbc.CardBody([
                                html.P(
                                    "Energieaanbod is de hoeveelheid energie die primair beschikbaar"+
                                    " komt voor verbruik in Nederland."
                                ),
                                html.P(
                                    "TPES staat voor 'Total Primary Energy Supply'"+
                                    " en wordt gemeten in petajoule. (ookwel PJ)"
                                ),
                                html.P(
                                    "TPES is de hoeveelheid energie die in het land primair beschikbaar komt"+
                                    " (invoer plus winning en voorraadonttrekking) minus de hoeveelheid die"+
                                    " het land verlaat (uitvoer en brandstofbunkering voor"+
                                    " grensoverschrijdend verkeer)."
                                )
                            ])
                        ],
                        className="m-4 pb-1 ", #style="height:560"
                    )
                ], xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3, className="mb-2 mt-2 pt-5 pb-2"
            )

        ], className="bg-dark g-0 mt-5" # pt-3 pb-5"
    ),
], className="pt-4")