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
from energyAppGlobalData import totalEnergyCategoriesWhole as totalEnergyCategories

##Set the layout for Page 2 "Energy Sources detailed"
# layout = html.Div([
#     dbc.Row(
#         [
#             dbc.Col(
#                 [
#                     html.H3("Energieaanbod in TPES over het jaar",
#                         className="text-center text-white"
#                     ),
#                     dcc.Dropdown(id='energie-aanbod-jaar',
#                         options= list(dfCbsEnergy['Perioden'].unique()), value='2020',
#                         className="mb-2 mt-2"
#                     ),
#                     dcc.Graph(id='energie-aanbod-per-drager'),
#                 ],
#                 xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="offset-1 mb-4 mt-2 g-4"
#             ),
#             dbc.Col(
#                 [
#                     html.H3("Detailoverzicht energie aanbod over het jaar",
#                         className="text-center text-white"
#                     ),
#                     dcc.Dropdown(id='energie-verdieping-opties',
#                         options = [
#                             'Totaal kool en koolproducten', 'Totaal aardoliegrondstoffen',
#                             'Totaal aardolieproducten', 'Hernieuwbare energie',
#                         ],
#                         value='Hernieuwbare energie', className="mb-2 mt-2"
#                     ),
#                     dcc.Graph(id='energie-aanbod-verdieping',
#                         # className="mb-3"
#                     )
#                 ],
#                 xs=12, sm=12,md=12,lg=5,xl=5,xxl=5, className="mb-4 mt-2 g-4"
#             ),
#         ],
#         className="bg-dark pt-2 pb-4 g-0"
#     )
# ])

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-aanbod-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020', className="mb-2 mt-2"
                    ),
                ], xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="offset-1 mt-2 pb-2 g-4"
            ),
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-verdieping-opties',
                        options = [
                            'Totaal kool en koolproducten', 'Totaal aardoliegrondstoffen',
                            'Totaal aardolieproducten', 'Hernieuwbare energie',
                        ],
                        value='Hernieuwbare energie', className="mb-2 mt-2"
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
                                "Energieaanbod in TPES over het jaar", className="text-center text-white"
                            ),
                        ],
                        xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-total-energy-sources-year-button",
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
                            dcc.Graph(id='energie-aanbod-per-drager'),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="bg-dark pb-2 g-0"
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
                                className="m-4 pb-1", style={"maxHeight": "520px", "overflow": "scroll"}
                            )
                        ],
                        xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3,
                        className="mb-2 mt-2 pb-2",
                    )
                ], className="bg-dark g-0"
            )
        ],
        id="total-energy-sources-year-collapse",
        is_open=True
    ),
    
    dbc.Row(
        [
            dbc.Button(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Detailoverzicht energie aanbod over het jaar",
                                className="text-center text-white"
                            ),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-detail-energy-sources-year-button",
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
                            dcc.Graph(id='energie-aanbod-verdieping'),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="bg-dark pb-2 g-0"
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
                                className="m-4 pb-1", style={"maxHeight": "520px", "overflow": "scroll"}
                            )
                        ],
                        xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3,
                        className="mb-2 mt-2 pb-2",
                    )
                ], className="bg-dark g-0"
            )
        ],
        id="detail-energy-sources-year-collapse",
        is_open=False
    ),
])

@callback(
    Output("total-energy-sources-year-collapse", "is_open"),
    [Input("collapse-total-energy-sources-year-button", "n_clicks")],
    [State("total-energy-sources-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("detail-energy-sources-year-collapse", "is_open"),
    [Input("collapse-detail-energy-sources-year-button", "n_clicks")],
    [State("detail-energy-sources-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


##Callback for energy sources totals over a year
@callback(
    Output('energie-aanbod-per-drager', 'figure'),
    Input('energie-aanbod-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy sources of year graph
    energySrcTotalSelect = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
    energySrcTotalSelect = energySrcTotalSelect[energySrcTotalSelect['Perioden']==str(selected_year)]
    energySrcTotaldf = energySrcTotalSelect.groupby(['Energiedragers']).sum()
    energySrcTotaldf = energySrcTotaldf.sort_values(by=['TotaalAanbodTPES_1'], ascending=True)

    ## Build the total energy sources of year graph
    fig = px.bar(
        x=energySrcTotaldf.index, y=energySrcTotaldf.TotaalAanbodTPES_1,
        labels={"y": "Totaalaanbod (TPES)", "x":"Energiedragers"},  height=600
    )
    fig.update_traces(marker_color='blue')
    fig.update_layout(
        font= dict(color="white"),
        plot_bgcolor= 'rgba(192,192,192,0.75)',
        paper_bgcolor= 'rgba(0,0,0,0)'
        
    )
    fig.update_xaxes(tickangle=-45)

    return fig

##Callback for energy sources detailed over a year
@callback(
    Output('energie-aanbod-verdieping', 'figure'),
    Input('energie-verdieping-opties', 'value'),
    Input('energie-aanbod-jaar', 'value')
)
def update_graph(selected_energy_source, selected_year):
    ## Select all energy carriers for the selected source
    if selected_energy_source == 'Totaal kool en koolproducten':
        energySelection = [
            'Antraciet', 'Cokeskool', 'Ketelkolen', 'Bruinkool', 'Cokesovencokes',
            'Bruinkoolbriketten', 'Steenkoolteer', 'Gasfabriekgas', 'Cokesovengas', 'Hoogovengas'
        ]
    elif selected_energy_source == 'Totaal aardoliegrondstoffen':
        energySelection = [
            'Ruwe aardolie', 'Aardgascondensaat', 'Additieven', 'Overige aardoliegrondstoffen'
        ]
    elif selected_energy_source == 'Totaal aardolieproducten':
        energySelection = [
            'Restgassen uit olie', 'Lpg', 'Nafta', 'Motorbenzine', 'Jetfuel op benzinebasis',
            'Vliegtuigbenzine', 'Vliegtuigkerosine', 'Overige kerosine (petroleum)',
            'Gas-, dieselolie en lichte stookolie', 'Zware stookolie', 'Terpentine en speciale benzine',
            'Smeermiddelen', 'Bitumen', 'Minerale wassen', 'Petroleumcokes', 'Overige aardolieproducten'
        ]
    elif selected_energy_source == 'Hernieuwbare energie':
        energySelection = [
            'Waterkracht', 'Windenergie op land', 'Windenergie op zee', 'Zonnewarmte', 'Zonnestroom',
            'Aardwarmte', 'Omgevingsenergie', 'Hernieuwbaar huishoudelijk afval', 
            'Vaste en vloeibare biomassa', 'Biogas'
        ]
    else :
        energySelection = []

    ## Prepare DataFrame for the Detail energy sources of year graph
    energySrcDetailSelect = dfCbsEnergy[ dfCbsEnergy['Energiedragers'].isin(energySelection)]
    energySrcDetailSelect = energySrcDetailSelect[energySrcDetailSelect['Perioden']==str(selected_year)]
    energySrcDetailDf = energySrcDetailSelect.groupby(['Energiedragers']).sum()
    energySrcDetailDf = energySrcDetailDf.sort_values(by=['TotaalAanbodTPES_1'], ascending=True)

    ## Build the detail energy sources of year graph
    fig = px.bar(
        x=energySrcDetailDf.index, y=energySrcDetailDf.TotaalAanbodTPES_1,
        labels={"y": "Totaalaanbod (TPES)", "x":"Energiedragers"}, height=600
    )
    fig.update_traces(marker_color='blue')
    fig.update_layout(
        plot_bgcolor= 'rgba(192,192,192,0.75)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        font= dict(color="white")
    )
    fig.update_xaxes(tickangle=-45)
    return fig