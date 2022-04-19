## Import dependency packages
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback

## Import all the pages
from pages import page1, page2, page3, page4, page5, page6, page7

## Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[{
        "name": "viewport", "content": "width=device-width, initial-scale=1.0",
    }]
)

## App layout
app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Energieaanbod tijdlijn",
                        href="/page1", className="text-black"
                    ),
                    dbc.DropdownMenuItem("Energieaanbod per jaar",
                        href="/page2", className="text-black"
                    ),
                ],
                nav=True,
                in_navbar=True,
                label="Energieaanbod",
                toggleClassName="text-white"
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Totaal verbruik tijdlijn",
                        href="/page3", className="text-black"
                    ),
                    dbc.DropdownMenuItem("Totaal verbruik per jaar",
                        href="/page4", className="text-black"
                    ),
                    dbc.DropdownMenuItem("Energieomzetting per jaar",
                        href="/page5", className="text-black pl-2"
                    ),
                    dbc.DropdownMenuItem("Eigen verbruik per jaar",
                        href="/page6", className="text-black pl-2"
                    ),
                    dbc.DropdownMenuItem("Finaal verbruik per jaar",
                        href="/page7", className="text-black pl-2"
                    ),
                ],
                    nav=True,
                    in_navbar=True,
                    label="Energieverbruik",
                    toggleClassName="text-white"
            ),
        ],
        brand="Dashboard energie in nederland", brand_href="/",
        brand_style={'color':'white'}, color="primary",
        className="text-center text-light",
    ),
    html.Div(
        [
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content', className="bg-light")
        ]
    )
])

## Callbacks for navigating the app
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return page1.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page3':
        return page3.layout
    elif pathname == '/page4':
        return page4.layout
    elif pathname == '/page5':
        return page5.layout
    elif pathname == '/page6':
        return page6.layout
    elif pathname == '/page7':
        return page7.layout
    else:
        return '404'

## Run the Dash app
app.run_server(port='8002')