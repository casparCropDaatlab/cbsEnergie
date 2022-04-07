from turtle import width
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback

import plotly
import plotly_express as px
import plotly.graph_objects as go

import pandas
from energyApp import dfCbsEnergy

# print(list(dfCbsEnergy.columns.values()))
# print(list(dfCbsEnergy['Energiedragers'].unique()))

## Categories for the total of energy sources
totalEnergyCategories = [
    'Totaal kool en koolproducten',
    'Totaal aardoliegrondstoffen en producten',
    'Aardgas',
    'Hernieuwbare energie',
    'Elektriciteit',
    'Warmte',
    'Kernenergie'
]

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Energieaanbod in TPES over het jaar", className="text-center text-white"),
            dcc.Dropdown(
                id='energei-aanbod-jaar',
                options= list(dfCbsEnergy['Perioden'].unique()),
                value='2020',
                className="mb-4 mt-2"
            ) ,
            dcc.Graph(id='energie-aanbod-per-drager'),
        ], xs=12, sm=12,md=12,lg=5,xl=5,xxl=5, className="offset-1 mb-2 mt-2"),
        dbc.Col([
            html.H3("Detailoverzicht energie aanbod over het jaar", className="text-center text-white"),
            dcc.Dropdown(
                id='energie-verdieping-opties',
                options = [
                    'Totaal kool en koolproducten',
                    'Totaal aardoliegrondstoffen',
                    'Totaal aardolieproducten',
                    'Hernieuwbare energie',
                ],
                value='Hernieuwbare energie',
                className="mb-4 mt-2"
            ),
            dcc.Graph(id='energie-aanbod-verdieping',className="mb-3")
        ], xs=12, sm=12,md=12,lg=5,xl=5,xxl=5, className="mb-2 mt-2"),
    ], className="mt-4 mb-2 bg-secondary"),
])

##Callbacks
@callback(
    Output('energie-aanbod-per-drager', 'figure'),
    Input('energei-aanbod-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy sources of year graph
    energySourcesTotalDfSelect = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    energySourcesTotalDfSelect = energySourcesTotalDfSelect[
        energySourcesTotalDfSelect['Perioden']==str(selected_year)
    ]
    energySourcesTotaldf = energySourcesTotalDfSelect.groupby(['Energiedragers']).sum()
    energySourcesTotaldf = energySourcesTotaldf.sort_values(
        by=['TotaalAanbodTPES_1'], ascending=True
    )
    ## Build the total energy sources of year graph
    fig = px.bar(
        y=energySourcesTotaldf.index,
        x=energySourcesTotaldf.TotaalAanbodTPES_1,
        labels={"x": "Totaalaanbod (TPES)", "y":"Energiedragers"},
        height=650
    )
    fig.update_traces(marker_color='darkgreen')
    return fig

@callback(
    Output('energie-aanbod-verdieping', 'figure'),
    Input('energie-verdieping-opties', 'value'),
    Input('energei-aanbod-jaar', 'value')
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

    ## Prepare DataFrame for the Detail energy sources of year graph
    energySourcesDetailDfSelect = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(energySelection)
    ]
    energySourcesDetailDfSelect = energySourcesDetailDfSelect[
        energySourcesDetailDfSelect['Perioden']==str(selected_year) 
    ]
    energySourcesDetailDf = energySourcesDetailDfSelect.groupby(['Energiedragers']).sum()
    energySourcesDetailDf = energySourcesDetailDf.sort_values(
        by=['TotaalAanbodTPES_1'], ascending=True
    )
    ## Build the detail energy sources of year graph
    fig = px.bar(
        y=energySourcesDetailDf.index,
        x=energySourcesDetailDf.TotaalAanbodTPES_1,
        labels={"x": "Totaalaanbod (TPES)", "y":"Energiedragers"},
        height=650
    )
    fig.update_traces(marker_color='darkgreen')
    return fig