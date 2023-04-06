import dash
from dash import Dash, html
from threading import Timer
import dash_bootstrap_components as dbc


port = 8055
host = '127.0.0.1'

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([

			        dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem(page['name'].upper(),href=page["relative_path"])
                        for page in dash.page_registry.values()
                        ],
                        label="Menu",
                        id = "ddmenu",
                    )
    
                    ], width=1, id='c1'),
                dbc.Col([
                    html.Img(src=dash.get_asset_url('Cial_D_B_Logo.png'), style={'width':'90%'})  
                ], width=3, id='c2'),
                dbc.Col([
                    html.Div(
                        html.H2( id='main_header', children='Productivity & Decision Management Tools'),
                        ),
                ], width=6, id='c3'),
            ], id='maenu_bar')])
        ),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(host=host, port=port, debug=False)