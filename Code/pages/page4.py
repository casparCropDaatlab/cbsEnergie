import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
import plotly
import plotly_express as px
import plotly.graph_objects as go

import sys
sys.path.insert(0, '/cbsEnergie/Code/pages/')
from energyAppGlobalData import dfCbsEnergy, totalEnergyCategories

##Set the layout for Page 2
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Energie verbruik over het jaar", className="text-center text-white"),
            dcc.Dropdown(
                id='energei-verbruik-jaar',
                options= list(dfCbsEnergy['Perioden'].unique()),
                value='2020',
                className="mb-4 mt-2"
            ) ,
            dcc.Graph(id='energie-verbruik-per-drager'),
        ], xs=12, sm=12,md=12,lg=5,xl=5,xxl=5, className="offset-1 mb-2 mt-2"),
        dbc.Col([
            html.H3("Detailoverzicht energie verbruik over het jaar", className="text-center text-white"),
            dcc.Dropdown(
                id='energie-verbruik-verdieping-opties',
                options = [
                    'Totaal kool en koolproducten',
                    'Totaal aardoliegrondstoffen',
                    'Totaal aardolieproducten',
                    'Hernieuwbare energie',
                ],
                value='Hernieuwbare energie',
                className="mb-4 mt-2"
            ),
            dcc.Graph(id='energie-verbruik-verdieping',className="mb-3")
        ], xs=12, sm=12,md=12,lg=5,xl=5,xxl=5, className="mb-2 mt-2"),
    ], className="mt-4 mb-2 bg-secondary"),
])

##Callbacks
@callback(
    Output('energie-verbruik-per-drager', 'figure'),
    Input('energei-verbruik-jaar', 'value')
)
def update_graph(selected_year):
    ## Prepare DataFrame for the total energy use of year graph
    energyUseTotalDfSelect = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    energyUseTotalDfSelect = energyUseTotalDfSelect[
        energyUseTotalDfSelect['Perioden']==str(selected_year)
    ]
    energyUseTotaldf = energyUseTotalDfSelect.groupby(['Energiedragers']).sum()
    energyUseTotaldf = energyUseTotaldf.sort_values(
        by=['TotaalEnergieverbruik_9'], ascending=True
    )
    ## Build the total energy use of year graph
    fig = px.bar(
        y=energyUseTotaldf.index,
        x=energyUseTotaldf.TotaalEnergieverbruik_9,
        labels={"x": "Totaalverbruik", "y":"Energiedragers"},
        height=650
    )
    fig.update_traces(marker_color='darkgreen')
    return fig

@callback(
    Output('energie-verbruik-verdieping', 'figure'),
    Input('energie-verbruik-verdieping-opties', 'value'),
    Input('energei-verbruik-jaar', 'value')
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

    ## Prepare DataFrame for the Detail energy use of year graph
    energyUseDetailDfSelect = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(energySelection)
    ]
    energyUseDetailDfSelect = energyUseDetailDfSelect[
        energyUseDetailDfSelect['Perioden']==str(selected_year) 
    ]
    energyUseDetailDf = energyUseDetailDfSelect.groupby(['Energiedragers']).sum()
    energyUseDetailDf = energyUseDetailDf.sort_values(
        by=['TotaalEnergieverbruik_9'], ascending=True
    )
    ## Build the detail energy use of year graph
    fig = px.bar(
        y=energyUseDetailDf.index,
        x=energyUseDetailDf.TotaalEnergieverbruik_9,
        labels={"x": "Totaalverbruik", "y":"Energiedragers"},
        height=650
    )
    fig.update_traces(marker_color='darkgreen')
    return fig