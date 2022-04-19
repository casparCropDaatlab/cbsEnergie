## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, State
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy
from energyAppGlobalData import totalEnergyCategoriesSplit as totalEnergyCategories

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
                "Energieomzetting is het veranderen van een energiedrager in  een andere. "+
                "Dit betekent het omzetten van brandstof in elektriciteit of warmte "+
                "of het omzetten van een brandstof in een andere soort brandstof."
            ),
            html.P(
                "Eigen verbruik is het verbruik van energie in installaties "+
                "voor de winning of omzetting van energie en het verbruik van "+
                "energie door bedrijven uit de energiesector. Dit betreft "+
                "alleen de benodigde hulpenergie, niet de inzet voor de energieomzetting zelf."
            ),
            html.P(
                "Finaal gebruik is het verbruik van energie buiten de energiesector. "+
                "Deze verbruikers kunnen worden gezien als de eindgebruikers van de energie."
            ),
        ])
    ],
    className="m-4 pb-1", style={"maxHeight": "520px", "overflow": "scroll"}
)

##Set the layout for Page 4 "Energy usage"
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-verbruik-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020', className="mb-2 mt-2"
                    ),
                ], xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="offset-1 mt-2 pb-2 g-4"
            ),
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-verbruik-verdieping-opties',
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
                                "Energie verbruik over het jaar", className="text-center text-white"
                            ),
                        ],
                        xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-total-energy-usage-year-button",
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
                            dcc.Graph(id='energie-verbruik-per-drager'),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="bg-dark pb-2 g-0"
                    ),
                    dbc.Col(
                        [
                            card
                        ], xs= 12, sm= 12, md= 12, lg= 3, xl= 3, xxl= 3, className="mb-2 mt-2 pb-2"
                    )
                ], className="bg-dark g-0"
            )
        ],
        id="total-energy-usage-year-collapse",
        is_open=True
    ),
    
    dbc.Row(
        [
            dbc.Button(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Detailoverzicht energie verbruik over het jaar",
                                className="text-center text-white"
                            ),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-detail-energy-usage-year-button",
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
                            dcc.Graph(id='energie-verbruik-verdieping'),
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
        id="detail-energy-usage-year-collapse",
        is_open=False
    ),
])

@callback(
    Output("total-energy-usage-year-collapse", "is_open"),
    [Input("collapse-total-energy-usage-year-button", "n_clicks")],
    [State("total-energy-usage-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("detail-energy-usage-year-collapse", "is_open"),
    [Input("collapse-detail-energy-usage-year-button", "n_clicks")],
    [State("detail-energy-usage-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

##Callback for the total energy use per year graph
@callback(
    Output('energie-verbruik-per-drager', 'figure'),
    Input('energie-verbruik-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy use of year graph
    energyUseTotalSelect = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
    energyUseTotalSelect = energyUseTotalSelect[energyUseTotalSelect['Perioden']==str(selected_year)]
    energyUseTotaldf = energyUseTotalSelect.groupby(['Energiedragers']).sum()
    energyUseTotaldf = energyUseTotaldf.sort_values(by=['TotaalEnergieverbruik_9'], ascending=True)

    ## Build the total energy use of year graph
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name="Totaalsaldo energieomzetting",
            x = energyUseTotaldf.index, y=energyUseTotaldf.TotaalSaldoEnergieomzetting_16
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal eigen verbruik",
            x = energyUseTotaldf.index, y=energyUseTotaldf.Totaal_19
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal finaal verbruik",
            x = energyUseTotaldf.index, y=energyUseTotaldf.TotaalFinaalVerbruik_27
        )
    )
    fig.add_trace(
        go.Bar(name="Verlies bij distributie",
            x = energyUseTotaldf.index, y = energyUseTotaldf.VerliezenBijDistributie_26
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal Energieverbruik",
            x = energyUseTotaldf.index, y = energyUseTotaldf.TotaalEnergieverbruik_9
        )
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

##Callback for the detailed energy use per year graph
@callback(
    Output('energie-verbruik-verdieping', 'figure'),
    Input('energie-verbruik-verdieping-opties', 'value'),
    Input('energie-verbruik-jaar', 'value')
)
def update_graph(selected_energy_source, selected_year):
    ## Get the selected energy carriers from the given input
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

    ## Prepare DataFrame for the Detail energy use of year graph
    energyUseDetailSelect = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(energySelection)]
    energyUseDetailSelect = energyUseDetailSelect[energyUseDetailSelect['Perioden']==str(selected_year)]
    energyUseDetailDf = energyUseDetailSelect.groupby(['Energiedragers']).sum()
    energyUseDetailDf = energyUseDetailDf.sort_values(by=['TotaalEnergieverbruik_9'], ascending=True)

    ## Build the detail energy use of year graph
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name="Totaalsaldo energieomzetting",
            x = energyUseDetailDf.index, y=energyUseDetailDf.TotaalSaldoEnergieomzetting_16
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal eigen verbruik",
            x = energyUseDetailDf.index, y=energyUseDetailDf.Totaal_19
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal finaal verbruik",
            x = energyUseDetailDf.index, y=energyUseDetailDf.TotaalFinaalVerbruik_27
        )
    )
    fig.add_trace(
        go.Bar(name="Verlies bij distributie",
            x = energyUseDetailDf.index, y = energyUseDetailDf.VerliezenBijDistributie_26
        )
    )
    fig.add_trace(
        go.Bar(name="Totaal Energieverbruik",
            x = energyUseDetailDf.index, y = energyUseDetailDf.TotaalEnergieverbruik_9
        )
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