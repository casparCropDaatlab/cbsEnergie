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

# TotaalFinaalVerbruik_27

# Totaal_28 -Finaal energieverbruik totaal

#   Totaal_29 --Nijverheid exclusief de energiesector
#       IJzerEnStaalindustrie_30
#       ChemieEnFarmaceutischeIndustrie_31
#       NonFerrometalenindustrie_32
#       Bouwmaterialenindustrie_33
#       Transportmiddelenindustrie_34
#       MetaalproductenEnMachineIndustrie_35
#       DelfstoffenwinningGeenOlieEnGas_36
#       VoedingsEnGenotmiddelenindustrie_37
#       PapierEnGrafischeIndustrie_38
#       Houtindustrie_39
#       Bouwnijverheid_40
#       TextielKledingEnLederindustrie_41
#       OverigeIndustrieEnOnbekend_42

#   Totaal_43 --Vervoertotaal
#       BinnenlandseLuchtvaart_44
#       Wegverkeer_45
#       Railverkeer_46
#       Pijpleidingen_47
#       BinnenlandseScheepvaart_48
#       Onbekend_49

#   Totaal_50  --Overige afnemers
#       DienstenAfvalWaterEnReparatie_51
#       Woningen_52
#       Landbouw_53
#       Visserij_54
#       Onbekend_55

# Totaal_56 -Niet energetisch gebruik totaal
#   NijverheidExclusiefDeEnergiesector_57
#   WaarvanChemieEnPetrochemie_58
#   Vervoer_59
#   OverigeAfnemers_60

def buildSelectedItemsGraph(figure, df, selection):
    for finalUsage in selection:
        try:
            txtList = finalUsage.split('_')
            txt = txtList[0]
            figure.add_trace(
                go.Bar(
                    name=txt,
                    x=df.index,
                    y=df[finalUsage]
                ),
            )
        except:
            print("Could not find the column named: "+finalUsage)
    return figure


## Eigen verbruik layout
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3(
                        "Finaal verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(
                        id='energie-finaal-verbruik-jaar',
                        options= list(dfCbsEnergy['Perioden'].unique()),
                        value='2020',
                        className="mb-4 mt-2"
                    ) ,
                    dcc.Graph(id='energie-finaal-verbruik-per-drager'),
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-2 mt-2"
            ),
            dbc.Col(
                [
                    html.H3(
                        "Detailoverzicht finaal verbruik over het jaar",
                        className="text-center text-white"
                    ),
                    dcc.Dropdown(
                        id='energie-finaal-verbruik-verdieping-opties',
                        options = [
                            'Nijverheid exclusief de energiesector',
                            'Vervoer',
                            'Overige afnemers',
                            'Niet energetisch gebruik',
                        ],
                        value='Nijverheid exclusief de energiesector',
                        className="mb-4 mt-2"
                    ),
                    dcc.Graph(id='energie-finaal-verbruik-verdieping',className="mb-3")
                ], 
                xs=10, sm=10,md=10,lg=10,xl=10,xxl=10,
                className="offset-1 mb-5 mt-2"
            ),
        ], className="mt-4 mb-2 bg-secondary"
    ),
])

## Callbacks
@callback(
    Output("energie-finaal-verbruik-per-drager", "figure"),
    Input("energie-finaal-verbruik-jaar", "value")
)
def update_graph(selected_year):
    
    finalUsageSelection = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    finalUsageSelection = finalUsageSelection[
        finalUsageSelection['Perioden']==str(selected_year)
    ]
    finalUsageDf = finalUsageSelection.groupby(['Energiedragers']).sum()
    finalUsageDf = finalUsageDf.sort_values(
        by=['TotaalFinaalVerbruik_27'], ascending=True
    )

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

    # for item in finalUsageDf.index:
    #     fig.add_vline(x=item, row="all")

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
    Output("energie-finaal-verbruik-verdieping", "figure"),
    Input("energie-finaal-verbruik-jaar", "value"),
    Input("energie-finaal-verbruik-verdieping-opties", "value")
)
def update_graph(selected_year, selected_option):

    fig = go.Figure()

    ## Prepare the dataframe for use
    finalUsageDataSelect = dfCbsEnergy[
        dfCbsEnergy['Energiedragers'].isin(totalEnergyCategories)
    ]
    finalUsageDataSelect = finalUsageDataSelect[
        finalUsageDataSelect['Perioden'] == str(selected_year)
    ]
    finalUsageDetailDf = finalUsageDataSelect.groupby(['Energiedragers']).sum()
    finalUsageDetailDf = finalUsageDetailDf.sort_values(
        by=['TotaalFinaalVerbruik_27'], ascending=True
    )

    ## Build the Graph for each item
    if selected_option == 'Nijverheid exclusief de energiesector':
        finalUsageSelection = [
            'IJzerEnStaalindustrie_30',
            'ChemieEnFarmaceutischeIndustrie_31',
            'NonFerrometalenindustrie_32',
            'Bouwmaterialenindustrie_33',
            'Transportmiddelenindustrie_34',
            'MetaalproductenEnMachineIndustrie_35',
            'DelfstoffenwinningGeenOlieEnGas_36',
            'VoedingsEnGenotmiddelenindustrie_37',
            'PapierEnGrafischeIndustrie_38',
            'Houtindustrie_39',
            'Bouwnijverheid_40',
            'TextielKledingEnLederindustrie_41',
            'OverigeIndustrieEnOnbekend_42'
        ]
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
    elif selected_option == 'Vervoer':
        finalUsageSelection = [
            'BinnenlandseLuchtvaart_44',
            'Wegverkeer_45',
            'Railverkeer_46',
            'Pijpleidingen_47',
            'BinnenlandseScheepvaart_48',
            'Onbekend_49'
        ]
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
    elif selected_option == 'Overige afnemers':
        finalUsageSelection = [
            'DienstenAfvalWaterEnReparatie_51',
            'Woningen_52',
            'Landbouw_53',
            'Visserij_54',
            'Onbekend_55'
        ]
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
    elif selected_option == 'Niet energetisch gebruik':
        finalUsageSelection = [
            'NijverheidExclusiefDeEnergiesector_57',
            'WaarvanChemieEnPetrochemie_58',
            'Vervoer_59',
            'OverigeAfnemers_60'
        ]
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
    else:
        finalUsageSelection = []
        fig = buildSelectedItemsGraph(fig, finalUsageDetailDf, finalUsageSelection)
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
