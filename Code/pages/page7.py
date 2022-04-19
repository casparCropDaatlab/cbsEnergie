## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy
from energyAppGlobalData import totalEnergyCategoriesSplit as totalEnergyCategories

## Function for building a graph based on selected list of columns
def buildSelectedItemsGraph(figure, df, selection):
    ## Loop through each selected column
    for finalUsage in selection:
        try:
            ## If the selected column is not empty
            txtList = finalUsage.split('_')
            txt = txtList[0]
            figure.add_trace(go.Bar(name=txt, x=df.index, y=df[finalUsage]))
        except:
            ## If the selected column is empty
            print("Could not find the column named: "+finalUsage)
    
    return figure

card = dbc.Card(
    [
        dbc.CardHeader([
            html.H5("Uitleg bij deze grafiek:")
        ]),
        dbc.CardBody([
            html.P(
                "Verbruik wordt gemeten in petajoules (ookwel PJ)"
            ),
            html.P(
                "Finaal gebruik is het verbruik van energie buiten de energiesector. "+
                "Deze verbruikers kunnen worden gezien als de eindgebruikers van de energie."
            )
        ])
    ],
    className="m-4 pb-1", style={"maxHeight": "520px", "overflow": "scroll"}
)

## Eigen verbruik layout
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-finaal-verbruik-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020', className="mb-2 mt-2"
                    ),
                ], xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="offset-1 mt-2 pb-2 g-4"
            ),
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-finaal-verbruik-verdieping-opties',
                        options = [
                            'Nijverheid exclusief de energiesector', 'Vervoer',
                            'Overige afnemers', 'Niet energetisch gebruik',
                        ],
                        value='Nijverheid exclusief de energiesector', className="mb-2 mt-2"
                    ),
                ], xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="mt-2 pb-2 g-4"
            )
        ], className="bg-light g-0"
    ),

    dbc.Row(
        [
            dbc.Button(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Finaal verbruik over het jaar", className="text-center text-white"
                            ),
                        ],
                        xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-total-energy-final-usage-year-button",
                className="mg-0",
                color="primary",
                n_clicks=0,
            ),
        ], className="bg-dark g-0"
    ),
    dbc.Collapse(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id='energie-finaal-verbruik-per-drager'),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="bg-dark pb-2 g-0"
                    ),
                    dbc.Col(
                        [
                            card
                        ],
                        xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3,
                        className="mb-2 mt-2 pb-2",
                    )
                ], className="bg-dark g-0"
            )
        ],
        id="total-energy-final-usage-year-collapse",
        is_open=True
    ),
    
    dbc.Row(
        [
            dbc.Button(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Detailoverzicht finaal verbruik over het jaar",
                                className="text-center text-white"
                            ),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-detail-energy-final-usage-year-button",
                className="mg-0",
                color="primary",
                n_clicks=0,
            ),
        ], className="bg-dark g-0 mt-4"
    ),
    dbc.Collapse(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id='energie-finaal-verbruik-verdieping'),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="bg-dark pb-2 g-0"
                    ),
                    dbc.Col(
                        [
                            card
                        ],
                        xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3,
                        className="mb-2 mt-2 pb-2",
                    )
                ], className="bg-dark g-0"
            )
        ],
        id="detail-energy-final-usage-year-collapse",
        is_open=False
    ),
])

@callback(
    Output("total-energy-final-usage-year-collapse", "is_open"),
    [Input("collapse-total-energy-final-usage-year-button", "n_clicks")],
    [State("total-energy-final-usage-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("detail-energy-final-usage-year-collapse", "is_open"),
    [Input("collapse-detail-energy-final-usage-year-button", "n_clicks")],
    [State("detail-energy-final-usage-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

## Callback "Finaal Verbruik totaal"
@callback(
    Output("energie-finaal-verbruik-per-drager", "figure"),
    Input("energie-finaal-verbruik-jaar", "value")
)
def update_graph(selected_year):
    ## Prepare dataframe for the graph
    finalUsageSelection = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
    finalUsageSelection = finalUsageSelection[finalUsageSelection['Perioden']==str(selected_year)]
    finalUsageDf = finalUsageSelection.groupby(['Energiedragers']).sum()
    finalUsageDf = finalUsageDf.sort_values(by=['TotaalFinaalVerbruik_27'], ascending=True)

    ## Make figure for the graph
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Nijverheid exclusief de energiesector",
            x=finalUsageDf.index,
            y=finalUsageDf['Totaal_29']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Vervoer",
            x=finalUsageDf.index,
            y=finalUsageDf['Totaal_43']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Overige afnemers",
            x=finalUsageDf.index,
            y=finalUsageDf['Totaal_50']
        ),
    )    
    fig.add_trace(
        go.Bar(
            name="Niet energetisch gebruik",
            x=finalUsageDf.index,
            y=finalUsageDf['Totaal_56']
        ),
    )

    ## Update graph layout for correct visualisation
    fig.update_layout(
        xaxis_title="Energiedragers",
        yaxis_title="Verbruik in PJ",
        barmode='group', height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0
        ),
        plot_bgcolor= 'rgba(192,192,192,0.75)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        font= dict(color="white")
    )
    fig.update_xaxes(tickangle=-45)
    return fig

## Callback "Finaal Verbruik Details"
@callback(
    Output("energie-finaal-verbruik-verdieping", "figure"),
    Input("energie-finaal-verbruik-jaar", "value"),
    Input("energie-finaal-verbruik-verdieping-opties", "value")
)
def update_graph(selected_year, selected_option):
    ## Prepare the figure
    fig = go.Figure()

    ## Prepare the dataframe for use in the graph
    finalUsageDataSelect = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
    finalUsageDataSelect = finalUsageDataSelect[finalUsageDataSelect['Perioden'] == str(selected_year)]
    finalUsageDetailDf = finalUsageDataSelect.groupby(['Energiedragers']).sum()
    finalUsageDetailDf = finalUsageDetailDf.sort_values(by=['TotaalFinaalVerbruik_27'], ascending=True)

    ## Build the Graph for each item
    if selected_option == 'Nijverheid exclusief de energiesector':
        ## Selection for "Nijverheid"
        finalUsageSelection = [
            'IJzerEnStaalindustrie_30', 'ChemieEnFarmaceutischeIndustrie_31', 
            'NonFerrometalenindustrie_32', 'Bouwmaterialenindustrie_33',
            'Transportmiddelenindustrie_34', 'MetaalproductenEnMachineIndustrie_35',
            'DelfstoffenwinningGeenOlieEnGas_36', 'VoedingsEnGenotmiddelenindustrie_37',
            'PapierEnGrafischeIndustrie_38', 'Houtindustrie_39', 'Bouwnijverheid_40',
            'TextielKledingEnLederindustrie_41', 'OverigeIndustrieEnOnbekend_42'
        ]

        ## Build the figure
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)

    elif selected_option == 'Vervoer':
        ## Selection for "Vervoer"
        finalUsageSelection = [
            'BinnenlandseLuchtvaart_44',
            'Wegverkeer_45',
            'Railverkeer_46',
            'Pijpleidingen_47',
            'BinnenlandseScheepvaart_48',
            'Onbekend_49'
        ]

        ## Build the figure
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)

    elif selected_option == 'Overige afnemers':
        ## Selection for "Overige afnemers"
        finalUsageSelection = [
            'DienstenAfvalWaterEnReparatie_51', 'Woningen_52',
            'Landbouw_53', 'Visserij_54', 'Onbekend_55'
        ]

        ## Build the figure
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)

    elif selected_option == 'Niet energetisch gebruik':
        ## Selection for "Niet energetisch gebruik"
        finalUsageSelection = [
            'NijverheidExclusiefDeEnergiesector_57', 'WaarvanChemieEnPetrochemie_58',
            'Vervoer_59', 'OverigeAfnemers_60'
        ]

        ## Build the figure 
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
    
    else:
        finalUsageSelection = []
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)

    ## Update graph layout for correct visualisation
    fig.update_layout(
        xaxis_title="Energiedragers",
        yaxis_title="Verbruik in PJ",
        barmode='group', height=600,
        legend=dict(
            orientation="h",
            yanchor="top", y=1.6,
            xanchor="left", x=0
        ),
        plot_bgcolor= 'rgba(192,192,192,0.75)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        font= dict(color="white")
    )
    fig.update_xaxes(tickangle=-45)

    return fig
