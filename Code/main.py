import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import plotly
import plotly_express as px
import plotly.graph_objects as go

import pandas
import cbsodata

cbsEnergyDataSet = cbsodata.get_data('83140NED')

