import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H2(id='page_title', children=''),
    html.Div(id='left_demo_list',children=['-'],),
    html.Div(children=[
            html.Ul(id='demo_list', 
                children=[ html.P(html.Font('''The different productivity & decision management tools can be accessed''',className='main_text')),
                    html.Li([html.Font('SQL Server Query:', className='list_item_descriptor'), html.P('''This demo queries a SQL server database directly
                             based on the parameters selected using dropdown menus.''', className='list_text')]),
                    html.Li([html.Font('External Libraries:', className='list_item_descriptor'), html.P('''The external libraries demos show how any JavaScript library 
                            can work with Dash, making the browser agreat tool for data visualizatiob, but also as a machine learning implementation platform thanks to 
                            TensorFlow.js''', className='list_text')]),
                    html.Li([html.Font('External API Integration:', className='list_item_descriptor'),  html.P('''Since Dask runs in a server or standalone with the help 
                            of Flask, it can connect to API services. This demo shows connection to two different APIs and how they can work sinergically''', className='list_text')]),
                    html.Li([html.Font('Data Quality and Completeness:', className='list_item_descriptor'),  html.P('''This demo is a prototype of a full working solution tha will 
                            be imlemented soon...''', className='list_text')]),
                ])
            ]),
    html.Div(id='right_demo_list',children=['-'],),
    ], id='homepage')