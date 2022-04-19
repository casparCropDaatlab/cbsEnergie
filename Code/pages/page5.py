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

card= dbc.Card(
    [
        dbc.CardHeader([
            html.H5("Uitleg bij deze grafiek:")
        ]),
        dbc.CardBody([
            html.P(
                "Energieomzetting wordt gemeten in petajoules (ookwel PJ)"
            ),
            html.P(
                "Voor de ingezette energiedragers is het saldo energieomzetting altijd positief."
            ),
            html.P(
                "Voor de geproduceerde energiedragers is het saldo altijd negatief. "+
                "Bij omzetting naar andere energiedragers wordt er immers meer van "+
                "geproduceerd dan ingezet."
            ),
            html.P(
                "Voor het totaal van alle energiedragers is het saldo de "+
                "hoeveelheid energie die verloren is gegaan bij de omzetting van energiedragers."
            )
        ])
    ],
    className="m-4 pb-1", style={"maxHeight": "520px", "overflow": "scroll"}
)

## Energieomzetting layout
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-omzet-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020', className="mb-2 mt-2"
                    ),
                ], xs=10, sm=10,md=10,lg=5,xl=5,xxl=5, className="offset-1 mt-2 pb-2 g-4"
            ),
            dbc.Col(
                [
                    dcc.Dropdown(id='energie-omzet-verdieping-opties',
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
                                "Energieomzetting over het jaar", className="text-center text-white"
                            ),
                        ],
                        xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-total-energy-conversion-year-button",
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
                            dcc.Graph(id='energie-omzet-per-drager'),
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
        id="total-energy-conversion-year-collapse",
        is_open=True
    ),
    
    dbc.Row(
        [
            dbc.Button(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Detailoverzicht energie omzet over het jaar",
                                className="text-center text-white"
                            ),
                        ],
                        xs=12, sm=12,md=12,lg=9,xl=9,xxl=9,
                        className="offset-1 g-0"
                    ),
                ],
                id="collapse-detail-energy-conversion-year-button",
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
                            dcc.Graph(id='energie-omzet-verdieping'),
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
        id="detail-energy-conversion-year-collapse",
        is_open=False
    ),
])

@callback(
    Output("total-energy-conversion-year-collapse", "is_open"),
    [Input("collapse-total-energy-conversion-year-button", "n_clicks")],
    [State("total-energy-conversion-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("detail-energy-conversion-year-collapse", "is_open"),
    [Input("collapse-detail-energy-conversion-year-button", "n_clicks")],
    [State("detail-energy-conversion-year-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


##Callback for "Energie omzetting" totals for the year
@callback(
    Output('energie-omzet-per-drager', 'figure'),
    Input('energie-omzet-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy conversion of year graph
    energyConvTselect = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)]
    energyConvTselect = energyConvTselect[energyConvTselect['Perioden']==str(selected_year)]
    energyConvTdf = energyConvTselect.groupby(['Energiedragers']).sum()
    energyConvTdf = energyConvTdf.sort_values(by=['TotaalSaldoEnergieomzetting_16'], ascending=True)

    ## Build the total energy conversion of year graph
    fig = go.Figure(data=[
        go.Bar(name="Totaal inzet",
            x=energyConvTdf.index, y=energyConvTdf['TotaalInzet_10']
        ),
        go.Bar(name="Totaal productie",
            x=energyConvTdf.index, y=energyConvTdf['TotaalProductie_13']
        ),
        go.Bar(name="Totaal saldo energieomzetting",
            x=energyConvTdf.index, y=energyConvTdf['TotaalSaldoEnergieomzetting_16']
        ),
    ])

    ## Update graph layout for correct visualisation
    fig.update_layout(
        xaxis_title="Energiedragers",
        yaxis_title="Omzetting in PJ",
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

## Callback for the "Energie omzet" detailed graph
@callback(
    Output('energie-omzet-verdieping', 'figure'),
    Input('energie-omzet-verdieping-opties', 'value'),
    Input('energie-omzet-jaar', 'value')
)
def update_graph(selected_energy_source, selected_year):
    ## Set the list of energy carriers based on the selected source
    if selected_energy_source == 'Totaal kool en koolproducten':
        energySelection = [
            'Antraciet', 'Cokeskool', 'Ketelkolen', 'Bruinkool', 'Cokesovencokes', 'Bruinkoolbriketten',
            'Steenkoolteer', 'Gasfabriekgas', 'Cokesovengas', 'Hoogovengas'
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

    ## Prepare DataFrame for the Detail energy conversion of year graph
    energyConvSel = dfCbsEnergy[dfCbsEnergy['Energiedragers'].isin(energySelection)]
    energyConvSel = energyConvSel[energyConvSel['Perioden']==str(selected_year)]
    energyConvDf = energyConvSel.groupby(['Energiedragers']).sum()
    energyConvDf = energyConvDf.sort_values(by=['TotaalSaldoEnergieomzetting_16'], ascending=True)
    
    ## Build the detail energy sources of year graph
    fig = go.Figure(data=[
        go.Bar(name="Totaal inzet",
            x=energyConvDf.index, y=energyConvDf['TotaalInzet_10']
        ),
        go.Bar(name="Totaal productie",
            x=energyConvDf.index, y=energyConvDf['TotaalProductie_13']
        ),
        go.Bar(name="Totaal saldo energieomzetting",
            x=energyConvDf.index, y=energyConvDf['TotaalSaldoEnergieomzetting_16']
        ),
    ])
    
    ## Update graph layout for correct visualisation
    fig.update_layout(
        xaxis_title="Energiedragers",
        yaxis_title="Omzetting in PJ",
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