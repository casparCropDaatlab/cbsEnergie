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

## Energieomzetting layout
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Energieomzetting over het jaar", className="text-center text-white"),
                    dcc.Dropdown(
                        id='energei-omzet-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020',
                        className="mb-4 mt-2"
                    ) ,
                    dcc.Graph(id='energie-omzet-per-drager'),
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-2 mt-2"
            ),
            dbc.Col(
                [
                    html.H3("Detailoverzicht energie omzet over het jaar", className="text-center text-white"),
                    dcc.Dropdown(
                        id='energie-omzet-verdieping-opties',
                        options = [
                            'Totaal kool en koolproducten',
                            'Totaal aardoliegrondstoffen',
                            'Totaal aardolieproducten',
                            'Hernieuwbare energie',
                        ],
                        value='Hernieuwbare energie',
                        className="mb-4 mt-2"
                    ),
                    dcc.Graph(id='energie-omzet-verdieping',className="mb-3")
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-5 mt-2"
            ),
        ],
        className="mt-4 mb-2 bg-secondary"
    ),
])

##Callbacks
@callback(
    Output('energie-omzet-per-drager', 'figure'),
    Input('energei-omzet-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy conversion of year graph
    energyConversionTotalSelection = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    energyConversionTotalSelection = energyConversionTotalSelection[
        energyConversionTotalSelection['Perioden']==str(selected_year)
    ]
    energyConversionTotalDf = energyConversionTotalSelection.groupby(['Energiedragers']).sum()
    energyConversionTotalDf = energyConversionTotalDf.sort_values(
        by=['TotaalAanbodTPES_1'], ascending=True
    )
    ## Build the total energy conversion of year graph
    fig = go.Figure(data=[
        go.Bar(
            name="Totaal inzet",
            x=energyConversionTotalDf.index,
            y=energyConversionTotalDf['TotaalInzet_10']
        ),
        go.Bar(
            name="Totaal productie",
            x=energyConversionTotalDf.index,
            y=energyConversionTotalDf['TotaalProductie_13']
        ),
        go.Bar(
            name="Totaal saldo energieomzetting",
            x=energyConversionTotalDf.index,
            y=energyConversionTotalDf['TotaalSaldoEnergieomzetting_16']
        ),
    ])
    fig.update_layout(barmode='group')

    return fig

@callback(
    Output('energie-omzet-verdieping', 'figure'),
    Input('energie-omzet-verdieping-opties', 'value'),
    Input('energei-omzet-jaar', 'value')
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
            'Steenkoolteer'
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

    ## Prepare DataFrame for the Detail energy conversion of year graph
    energyConversionSelection = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(energySelection)
    ]
    energyConversionSelection = energyConversionSelection[
        energyConversionSelection['Perioden']==str(selected_year) 
    ]
    energyConversionDf = energyConversionSelection.groupby(['Energiedragers']).sum()
    energyConversionDf = energyConversionDf.sort_values(
        by=['TotaalAanbodTPES_1'], ascending=True
    )
    ## Build the detail energy sources of year graph
    fig = go.Figure(data=[
        go.Bar(
            name="Totaal inzet",
            x=energyConversionDf.index,
            y=energyConversionDf['TotaalInzet_10']
        ),
        go.Bar(
            name="Totaal productie",
            x=energyConversionDf.index,
            y=energyConversionDf['TotaalProductie_13']
        ),
        go.Bar(
            name="Totaal saldo energieomzetting",
            x=energyConversionDf.index,
            y=energyConversionDf['TotaalSaldoEnergieomzetting_16']
        ),
    ])
    fig.update_layout(barmode='group')

    return fig