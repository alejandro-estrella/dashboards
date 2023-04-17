import dash
import os
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import State
import pandas as pd
from dash.dependencies import Input, Output
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import text
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import json
from dash_extensions import DeferScript


app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

host = (os.environ.get('SQLHOST'))
username = (os.environ.get('SQLUSER_CU'))
password = (os.environ.get('SQLPASS_CU'))
connection_url = URL.create("mssql+pymssql", username=username, password=password, host=host, database='cherishedUniverse')
dbEngine = create_engine(connection_url)

dbSession = sessionmaker(bind=dbEngine)
db = dbSession()

def readColumn(db, query,column):       
    sqlQuery = text(query)
    with dbEngine.connect() as msSQLConn:
        result = msSQLConn.execute(sqlQuery)
        if result:
            df = pd.DataFrame(result, columns=[f'{column}'])
            return df

def readTable(db, query):       
    sqlQuery = text(query)
    with dbEngine.connect() as msSQLConn:
        result = msSQLConn.execute(sqlQuery)
        if result:
            df = pd.DataFrame(result)
            return df
            
def queryByPeriod(tier, period, country):
    # print(tier)
    # print(period)
    # print(country)

    if period == 'Past due':
        qPeriod = 1
    elif period == 'Before 30 days':
        qPeriod = 2
    elif period == 'Next 30 days':
        qPeriod = 3
    elif period == 'Next 31 to 60 days':
        qPeriod = 4
    elif period == 'Next 61 to 90 days':
        qPeriod = 5
    elif period == 'More than 90 days':
        qPeriod = 6

    if country == 'Argentina':
        qCountry = 1
    elif country == 'Brazil':
        qCountry = 2
    elif country == 'Chile':
        qCountry = 3
    elif country == 'Mexico':
        qCountry = 4
    elif country == 'Peru':
        qCountry = 5

    query = f'''SELECT [Duns_No],[abCompanyName]
                FROM [cherishedUniverse].[dbo].[cherishedUniverseStatus]
                WHERE [countryId] = {qCountry} AND [tierId] = {tier} AND [statusId] = {qPeriod}'''
    
    df = readTable(db, query)

    return df 



query = '''SELECT DISTINCT B.[countryName]
  FROM [cherishedUniverse].[dbo].[cherishedUniverseAttributes] AS A
  LEFT JOIN [cherishedUniverse].[dbo].[countries] AS B
  ON A.[countryId] = B.id'''

countries = readTable(db, query)

country_list = countries['countryName'].to_list()

dash.register_page(__name__)

layout = html.Div(children=[
    html.Br(),
    html.H2(id='page_title', children='Cherished Universe Analysis & Follow Up'),
    html.Div([
        dcc.Dropdown(id = 'country-dd', placeholder='Country name...', className='dd', options=[
                {'label': i, 'value': i} for i in country_list
                ]),
        dbc.Button("Search", id="cherished-button", className="button1", n_clicks=0)
    ],id='options'),
	html.Div([
        html.Div(children=[html.Span(children=[html.Font('TIER', className='title3')])], className='grid_title_1'),
        html.Div(children=[html.Span(children=[html.Font('DUNS QUANTITY', className='title3')])], className='grid_title_2'),
        html.Div(children=[html.Span(children=[html.Font('PAST DUE', className='title3')])], className='grid_title_3'),
        html.Div(children=[html.Span(children=[html.Font('TO BE UPDATED', className='title3')])], className='grid_title_4'),
        html.Div(children=[html.Span(children=[html.Font('1', className='title1')])], className='tier_row_1'),
        html.Div(children=[html.Span(children=[html.Font('2', className='title1')])], className='tier_row_2'),
        html.Div(children=[html.Span(children=[html.Font('3', className='title1')])], className='tier_row_3'),
        html.Div(children=[html.Span(children=[html.Font('', className='title1')]),
                           html.Br(),
                           html.Span(children=[], id='T1')], className='tier1_1'),
        html.Div(children=[dcc.Graph(id='chart1_1',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier1_2'),
        html.Div(children=[dcc.Graph(id='chart2_1',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier1_3'),
        html.Div(children=[html.Span(children=[html.Font('', className='title1')]),
                           html.Br(),
                           html.Span(children=[], id='T2')], className='tier2_1'),
        html.Div(children=[dcc.Graph(id='chart1_2',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier2_2'),
        html.Div(children=[dcc.Graph(id='chart2_2',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier2_3'),
        html.Div(children=[html.Span(children=[html.Font('', className='title1')]),
                           html.Br(),
                           html.Span(children=[], id='T3')], className='tier3_1'),
        html.Div(children=[dcc.Graph(id='chart1_3',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier3_2'),
        html.Div(children=[dcc.Graph(id='chart2_3',className= 'grph1', figure={'data': [], 'layout': {
            'xaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
            'yaxis': {'showgrid':False, 'showline':False, 'showticklabels':False, 'zeroline':False},
         }}, config={'displayModeBar': False})], className='tier3_3')
    ],id='grid-output'),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal1_title'),dbc.Button("Close Window", id="Modal1-close", className="me-2", n_clicks=0),],id='tier1Modal1Header'),
                        html.Div( children=[],id='tier1Modalb'),
                        ],
                        className='csvDiv2'),
                        ],
                        id='tier1Modal', className='csvDiv', style={'display':'none'}),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal2_title'),dbc.Button("Close Window", id="Modal2-close", className="me-2", n_clicks=0)],id='tier1Modal2Header'),
                        html.Div( children=[],id='tier2Modalb'),
                        ],
                        className='csvDiv2'),
                        ],
                        id='tier2Modal', className='csvDiv', style={'display':'none'}),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal3_title'),dbc.Button("Close Window", id="Modal3-close", className="me-2", n_clicks=0)],id='tier1Modal3Header'),
                        html.Div( children=[],id='tier3Modalb'),
                        ],
                        className='csvDiv2'),
                        ],
                        id='tier3Modal', className='csvDiv', style={'display':'none'}),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal4_title'),dbc.Button("Close Window", id="Modal4-close", className="me-2", n_clicks=0)],id='tier1Modal4Header'),
                        html.Div( children=[],id='tier4Modalb'),
                        ],
                        className='csvDiv2'),
                        ]
                        ,id='tier4Modal', className='csvDiv', style={'display':'none'}),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal5_title'),dbc.Button("Close Window", id="Modal5-close", className="me-2", n_clicks=0)],id='tier2Modal5Header'),
                        html.Div( children=[],id='tier5Modalb'),
                        ],
                        className='csvDiv2'),
                        ]
                        ,id='tier5Modal', className='csvDiv', style={'display':'none'}),
    html.Div( children=[
                        html.Div( children=[
                        html.Div( children=[html.Div( children=[], id='modal6_title'),dbc.Button("Close Window", id="Modal6-close", className="me-2", n_clicks=0)],id='tier3Modal6Header'),
                        html.Div( children=[],id='tier6Modalb'),
                        ],
                        className='csvDiv2'),
                        ]
                        ,id='tier6Modal', className='csvDiv', style={'display':'none'}),

    DeferScript(src='/assets/main.js')
],id='main'),


@callback(
    Output(component_id='tier1Modalb', component_property='children'),
    Output(component_id='tier1Modal', component_property='style'),
    Output(component_id='Modal1-close', component_property='n_clicks'),
    Output(component_id='modal1_title', component_property='children'),
    Output(component_id='chart2_1', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart2_1', component_property='clickData'),
    Input(component_id='Modal1-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data1(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    pData = data[0]['x']
    period_data = queryByPeriod(1, pData, country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns], style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black'}, style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold',
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    title = pData[0].lower() + pData[1:]
    output.append(html.Font(f'{country} Tier 1 - To be updated in {title}', className='title4'))
    output.append(None)
    return  output

@callback(
    Output(component_id='tier2Modalb', component_property='children'),
    Output(component_id='tier2Modal', component_property='style'),
    Output(component_id='Modal2-close', component_property='n_clicks'),
    Output(component_id='modal2_title', component_property='children'),
    Output(component_id='chart2_2', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart2_2', component_property='clickData'),
    Input(component_id='Modal2-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data2(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    pData = data[0]['x']
    period_data = queryByPeriod(2, pData, country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns],style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black'}, style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold'
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    title = pData[0].lower() + pData[1:]
    output.append(html.Font(f'{country} Tier 2 - To be updated in {title}', className='title4'))
    output.append(None)
    return  output

@callback(
    Output(component_id='tier3Modalb', component_property='children'),
    Output(component_id='tier3Modal', component_property='style'),
    Output(component_id='Modal3-close', component_property='n_clicks'),
    Output(component_id='modal3_title', component_property='children'),
    Output(component_id='chart2_3', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart2_3', component_property='clickData'),
    Input(component_id='Modal3-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data3(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    pData = data[0]['x']
    period_data = queryByPeriod(3, pData, country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns],style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black' },style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold'
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    title = pData[0].lower() + pData[1:]
    output.append(html.Font(f'{country} Tier 3 - To be updated in {title}', className='title4'))
    output.append(None)
    return  output

@callback(
    Output(component_id='tier4Modalb', component_property='children'),
    Output(component_id='tier4Modal', component_property='style'),
    Output(component_id='Modal4-close', component_property='n_clicks'),
    Output(component_id='modal4_title', component_property='children'),
    Output(component_id='chart1_1', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart1_1', component_property='clickData'),
    Input(component_id='Modal4-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data4(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    curve = data[0]['curveNumber']
    if curve == 0:
        return None
    period_data = queryByPeriod(1, 'Past due', country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns], style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black'}, style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold',
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    output.append(html.Font(f'{country} Tier 1 - Past due', className='title4'))
    output.append(None)
    return  output

@callback(
    Output(component_id='tier5Modalb', component_property='children'),
    Output(component_id='tier5Modal', component_property='style'),
    Output(component_id='Modal5-close', component_property='n_clicks'),
    Output(component_id='modal5_title', component_property='children'),
    Output(component_id='chart1_2', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart1_2', component_property='clickData'),
    Input(component_id='Modal5-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data5(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    curve = data[0]['curveNumber']
    if curve == 0:
        return None
    period_data = queryByPeriod(2, 'Past due', country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns], style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black'}, style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold',
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    output.append(html.Font(f'{country} Tier 2 - Past due', className='title4'))
    output.append(None)
    return  output

@callback(
    Output(component_id='tier6Modalb', component_property='children'),
    Output(component_id='tier6Modal', component_property='style'),
    Output(component_id='Modal6-close', component_property='n_clicks'),
    Output(component_id='modal6_title', component_property='children'),
    Output(component_id='chart1_3', component_property='clickData'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='chart1_3', component_property='clickData'),
    Input(component_id='Modal6-close', component_property='n_clicks'),
    prevent_initial_call=True
    )

def display_click_data6(country, clickData,n_clicks):
    output = []
    if n_clicks > 0:
        output = []
        output.append('')
        output.append({'display': 'none'})
        output.append(0)
        output.append('')
        output.append(None)
        return  output
    if not clickData:
        raise PreventUpdate
    data = clickData['points']
    curve = data[0]['curveNumber']
    if curve == 0:
        return None
    period_data = queryByPeriod(3, 'Past due', country )
    table = dash_table.DataTable(data=period_data.to_dict('records'), columns=[{"Duns_No": i, "abCompanyNam": i,"id": i} for i in period_data.columns], style_cell={'textAlign': 'left','font-size':'1.5vh', 'border': '1px solid black'}, style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
            'backgroundColor': 'rgb(18, 169, 219)',
            'fontWeight': 'bold',
        },
         export_format="csv")
    output.append(table)
    output.append({'display': 'flex'})
    output.append(0)
    output.append(html.Font(f'{country} Tier 3 - Past due', className='title4'))
    output.append(None)
    return  output


@callback(
    Output(component_id='T1', component_property='children'),
    Output(component_id='T2', component_property='children'),
    Output(component_id='T3', component_property='children'),
    Output(component_id='chart1_1', component_property='figure'),
    Output(component_id='chart1_2', component_property='figure'),
    Output(component_id='chart1_3', component_property='figure'),
    Output(component_id='chart2_1', component_property='figure'),
    Output(component_id='chart2_2', component_property='figure'),
    Output(component_id='chart2_3', component_property='figure'),
    State(component_id='country-dd', component_property='value'),
    Input(component_id='cherished-button', component_property='n_clicks'),
    prevent_initial_call=True
)

def get_tier_data(country, n_clicks):

    data = []
    if n_clicks == 0:
        raise PreventUpdate
    elif country is None:
        return None
    else:
        sql = f'''
        SELECT A.[id]
	          ,B.[countryName]
              ,[tierId]
              ,[numDuns]
        FROM [cherishedUniverse].[dbo].[cherishedUniverseSummary] AS A
        LEFT JOIN [cherishedUniverse].[dbo].[countries] AS B
        ON A.[countryId] = B.id
        WHERE B.[countryName] = '{country}'
        '''
        tiers_data = readTable(db, sql)

        sql = f'''
        SELECT A.[id]
            ,B.[countryName]
            ,[countryId]
            ,[tierId]
            ,[statusId]
            ,[statusDesc]
            ,[numDuns]
            ,[updateDate]
        FROM [cherishedUniverse].[dbo].[cherishedUniverseStatusSummary] AS A
        LEFT JOIN [cherishedUniverse].[dbo].[countries] AS B
        ON A.[countryId] = B.id
        WHERE B.[countryName] = '{country}'
        '''
        charts_data = readTable(db, sql)

        for tier in tiers_data.itertuples():
            data.append('{:,}'.format(tier.numDuns))

        past_due=charts_data.query('statusDesc == "Past due"')[['tierId','numDuns']]
        current=pd.DataFrame(charts_data.query('statusDesc != "Past due"')[['tierId','numDuns']].groupby(['tierId']).sum())
        single_barchar_data = current.merge(past_due, on='tierId', how='left').rename(columns={"numDuns_x": "upToDate", "numDuns_y": "pastDue"})
        multi_barchar_data = charts_data.query('statusDesc != "Past due" and statusDesc != "Missing"')

        # print(past_due)
        # print(current)
        # print(single_barchar_data)
        # print(multi_barchar_data)

        for row in single_barchar_data.itertuples():
                if (row.upToDate+row.pastDue) == 0:
                    pctutd = 0
                    pctpd = 0
                else:
                    pctutd="{:.2%}".format(row.upToDate/(row.upToDate+row.pastDue))
                    pctpd="{:.2%}".format(row.pastDue/(row.upToDate+row.pastDue))
                fig= go.Figure()
                fig.add_trace(go.Bar(
                    y=[row.upToDate],
                    name = '',
                    hovertemplate=f'<br>Up to date : {pctutd}',
                    hoverlabel= {'bgcolor' : 'white', 'font': {'color': 'green', 'size':24}},
                    marker={'color':'green'},
                    opacity=0.5       
                    ))
                fig.add_trace(go.Bar(
                    y=[row.pastDue],
                    name = '',
                    hovertemplate=f'<br>Past due: {pctpd}',
                    hoverlabel= {'bgcolor' : 'white', 'font': {'color': 'red', 'size':24}},
                    hovertext= '',
                    marker={'color':'red'},
                    opacity=0.5,
                    ))
                fig.update_layout(
                    xaxis=dict(
                        showgrid=False,
                        showline=False,
                        showticklabels=False,
                        zeroline=False,
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showline=False,
                        showticklabels=False,
                        zeroline=False,
                    ),
                    barmode='stack',
                    paper_bgcolor='rgb(255, 255, 255)',
                    plot_bgcolor='rgb(255, 255, 255)',
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    clickmode='event',
                )
                data.append(fig)

        for x in range(3):
            multi_barchar_data2= multi_barchar_data.query(f'tierId == {x+1}')
            labels = list(multi_barchar_data2['statusDesc'])
            bar_data = multi_barchar_data2.numDuns.to_list()
            fig= go.Figure()
            fig.add_trace(go.Bar(
                x= ['Before 30 days',
                    'Next 30 days',
                    'Next 31 to 60 days',
                    'Next 61 to 90 days',
                    'More than 90 days'],
                y= bar_data,
                text = bar_data,
                textfont=dict(color='black', size=20),
                marker=dict(color=['orange','yellow','green','blue','lightgray']),
                opacity=0.8
                ))
            fig.update_layout(
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    zeroline=False,
                ),
                yaxis=dict(
                    showgrid=False,
                    showline=False,
                    showticklabels=False,
                    zeroline=False,
                ),
                barmode='stack',
                paper_bgcolor='rgb(255, 255, 255)',
                plot_bgcolor='rgb(255, 255, 255)',
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                clickmode='event',
                font=dict(
                    size=14 ,
                    color="black"
                    )
            )
            data.append(fig)

        return data
    
