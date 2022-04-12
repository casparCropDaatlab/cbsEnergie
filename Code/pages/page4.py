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

##Set the layout for Page 4 "Energy usage"
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Energie verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(id='energei-verbruik-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020', className="mb-4 mt-2"
                    ) ,
                    dcc.Graph(id='energie-verbruik-per-drager'),
                ], width=10, className="offset-1 mb-2 mt-2"
            ),
            dbc.Col(
                [
                    html.H3("Detailoverzicht energie verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(id='energie-verbruik-verdieping-opties',
                        options = [
                            'Totaal kool en koolproducten', 'Totaal aardoliegrondstoffen',
                            'Totaal aardolieproducten', 'Hernieuwbare energie',
                        ],
                        value='Hernieuwbare energie', className="mb-4 mt-2"
                    ),
                    dcc.Graph(id='energie-verbruik-verdieping', className="mb-3")
                ], width=10, className="offset-1 mb-2 mt-2"
            ),
        ], className="mt-4 mb-2 bg-secondary"
    ),
])

##Callback for the total energy use per year graph
@callback(
    Output('energie-verbruik-per-drager', 'figure'),
    Input('energei-verbruik-jaar', 'value')
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
            xanchor="right", x=1
        ),
    )

    return fig

##Callback for the detailed energy use per year graph
@callback(
    Output('energie-verbruik-verdieping', 'figure'),
    Input('energie-verbruik-verdieping-opties', 'value'),
    Input('energei-verbruik-jaar', 'value')
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
            xanchor="right", x=1
        ),
    )
    
    return fig