import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H2(id='page_title', children=''),
    html.Div(id='left_demo_list',children=['-'],),
    html.Div(children=[
            html.Ul(id='demo_list', 
                children=[ 
                ])
            ]),
    html.Div(id='right_demo_list',children=['-'],),
    ], id='homepage')