import pandas as pd
import cbsodata as cbs

##Script for wrangling some data to be used in a PowerBI dashboard

## Get the CBS energy data
baseCbsEnergyDf = pd.DataFrame(cbs.get_data('83140NED'))