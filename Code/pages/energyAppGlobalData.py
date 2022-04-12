import pandas
import cbsodata

## Get the CBS energy data
dfCbsEnergy = pandas.DataFrame(cbsodata.get_data('83140NED'))


# dfCbsColumns = dfCbsEnergy.columns
# for col in dfCbsColumns:
#     print(col)
    
# print(list(dfCbsEnergy['Energiedragers'].unique()))


##Set categories for totals
totalEnergyCategories = [
    'Totaal kool en koolproducten',
    'Totaal aardoliegrondstoffen',
    'Totaal aardolieproducten',
    'Aardgas',
    'Hernieuwbare energie',
    'Elektriciteit',
    'Warmte',
    'Kernenergie'
]