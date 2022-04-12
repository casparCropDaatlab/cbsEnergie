## Import dependency packages
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback
import plotly
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy, totalEnergyCategories

## Eigen verbruik layout
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3(
                        "Eigen verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(
                        id='energie-eigen-gebruik-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020',
                        className="mb-4 mt-2"
                    ) ,
                    dcc.Graph(id='eigen-energie-verbruik-per-drager'),
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-2 mt-2"
            ),
            dbc.Col(
                [
                    html.H3(
                        "Detailoverzicht eigen verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(
                        id='energie-eigen-verbruik-verdieping-opties',
                        options = [
                            'Totaal kool en koolproducten',
                            'Totaal aardoliegrondstoffen',
                            'Totaal aardolieproducten',
                            'Hernieuwbare energie',
                        ],
                        value='Hernieuwbare energie',
                        className="mb-4 mt-2"
                    ),
                    dcc.Graph(id='energie-eigen-verbruik-verdieping',className="mb-3")
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-5 mt-2"
            ),
        ], className="mt-4 mb-2 bg-secondary"
    ),
])

## Callbacks for the graphs
@callback(
    Output("eigen-energie-verbruik-per-drager", 'figure'),
    Input("energie-eigen-gebruik-jaar", 'value')
)
def update_graph(selected_year):
    ## Get the dataframe for own usage 'Totaal_19'
    energyUsageSelection = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    energyUsageSelection = energyUsageSelection[
        energyUsageSelection['Perioden']==str(selected_year) 
    ]
    energyUsageDf = energyUsageSelection.groupby(['Energiedragers']).sum()
    energyUsageDf = energyUsageDf.sort_values(
        by=['Totaal_19'], ascending=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Elektriciteit en warmteproductie",
            x=energyUsageDf.index,
            y=energyUsageDf['ElektriciteitsEnWarmteproductie_20']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Winning van olie & gas",
            x=energyUsageDf.index,
            y=energyUsageDf['WinningVanOlieEnGas_21']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Cokesfabrieken_22",
            x=energyUsageDf.index,
            y=energyUsageDf['Cokesfabrieken_22']
        ),
    )    
    fig.add_trace(
        go.Bar(
            name="Hoogovens",
            x=energyUsageDf.index,
            y=energyUsageDf['Hoogovens_23']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Olieraffinage installaties",
            x=energyUsageDf.index,
            y=energyUsageDf['OlieraffinageInstallaties_24']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Overige installaties",
            x=energyUsageDf.index,
            y=energyUsageDf['OverigeInstallaties_25']
        ),
    )

    fig.update_layout(
        barmode='group',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

@callback(
    Output('energie-eigen-verbruik-verdieping', 'figure'),
    Input('energie-eigen-verbruik-verdieping-opties', 'value'),
    Input('energie-eigen-gebruik-jaar', 'value')
)
def update_graph(selected_energy_source, selected_year):
    if selected_energy_source == 'Totaal kool en koolproducten':
        energySelection = [
            'Antraciet',
            'Cokeskool',
            'Ketelkolen',
            'Bruinkool',
            'Cokesovencokes',
            'Bruinkoolbriketten',
            'Steenkoolteer',
            'Gasfabriekgas',
            'Cokesovengas',
            'Hoogovengas'
        ]
    elif selected_energy_source == 'Totaal aardoliegrondstoffen':
        energySelection = [
            'Ruwe aardolie',
            'Aardgascondensaat',
            'Additieven',
            'Overige aardoliegrondstoffen'
        ]
    elif selected_energy_source == 'Totaal aardolieproducten':
        energySelection = [
            'Restgassen uit olie',
            'Lpg',
            'Nafta',
            'Motorbenzine',
            'Jetfuel op benzinebasis',
            'Vliegtuigbenzine',
            'Vliegtuigkerosine',
            'Overige kerosine (petroleum)',
            'Gas-, dieselolie en lichte stookolie',
            'Zware stookolie',
            'Terpentine en speciale benzine',
            'Smeermiddelen',
            'Bitumen',
            'Minerale wassen',
            'Petroleumcokes',
            'Overige aardolieproducten'
        ]
    elif selected_energy_source == 'Hernieuwbare energie':
        energySelection = [
            'Waterkracht',
            'Windenergie op land',
            'Windenergie op zee',
            'Zonnewarmte',
            'Zonnestroom',
            'Aardwarmte',
            'Omgevingsenergie',
            'Hernieuwbaar huishoudelijk afval',
            'Vaste en vloeibare biomassa',
            'Biogas'
        ]
    else :
        energySelection = []

    ## Prepare DataFrame for the Detail own usage energy of year graph
    energyUsageSelection = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(energySelection)
    ]
    energyUsageSelection = energyUsageSelection[
        energyUsageSelection['Perioden']==str(selected_year) 
    ]
    energyUsageDf = energyUsageSelection.groupby(['Energiedragers']).sum()
    # energyUsageDf = energyUsageDf.sort_values(
    #     by=[str(selected_energy_source)], ascending=True
    # )
    ## Build the detail energy sources of year graph
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Elektriciteit en warmteproductie",
            x=energyUsageDf.index,
            y=energyUsageDf['ElektriciteitsEnWarmteproductie_20']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Winning van olie & gas",
            x=energyUsageDf.index,
            y=energyUsageDf['WinningVanOlieEnGas_21']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Cokesfabrieken",
            x=energyUsageDf.index,
            y=energyUsageDf['Cokesfabrieken_22']
        ),
    )    
    fig.add_trace(
        go.Bar(
            name="Hoogovens",
            x=energyUsageDf.index,
            y=energyUsageDf['Hoogovens_23']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Olieraffinage installaties",
            x=energyUsageDf.index,
            y=energyUsageDf['OlieraffinageInstallaties_24']
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Overige installaties",
            x=energyUsageDf.index,
            y=energyUsageDf['OverigeInstallaties_25']
        ),
    )
    fig.update_layout(
        barmode='group',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig