## Import dependency packages
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy, totalEnergyCategories

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

##Callback for "Energie omzetting" totals for the year
@callback(
    Output('energie-omzet-per-drager', 'figure'),
    Input('energei-omzet-jaar', 'value')
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
            xanchor="right", x=1
        )
    )

    return fig

## Callback for the "Energie omzet" detailed graph
@callback(
    Output('energie-omzet-verdieping', 'figure'),
    Input('energie-omzet-verdieping-opties', 'value'),
    Input('energei-omzet-jaar', 'value')
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
            xanchor="right", x=1
        )
    )

    return fig