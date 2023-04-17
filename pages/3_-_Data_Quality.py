import dash
from dash import html, dcc, dash_table
from dash import html, dcc, callback, Input, Output
from dash.dependencies import State
import pandas as pd
from dash.dependencies import Input
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import text
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

host = 'NJ-SQL001.cialdnb.com'
username = 'dataquality'
password = 'Ajax5647'
connection_url = URL.create("mssql+pymssql", username=username, password=password, host=host, database='dataQuality')
dbEngine2 = create_engine(connection_url)

dbSession2 = sessionmaker(bind=dbEngine2)
db2 = dbSession2()
output_list = []

def readTable(query):       
    sqlQuery = text(query)
    with dbEngine2.connect() as msSQLConn:
        result = msSQLConn.execute(sqlQuery)
        if result:
            df = pd.DataFrame(result)
            return df

query = '''
    SELECT A.[id]
        ,A.[year]
        ,A.[week]
        ,A.[dataElement]
        ,A.[rowsPopulated]
        ,A.[rowsNonPopulated]
        ,A.[rowsPopulatedPct]
        ,A.[rowsNonPopulatedPct]
        ,A.[evalDate]
        ,B.[countryCode]
        ,B.[countryName]
        ,C.[universeDesc]
        ,D.[desc]
    FROM [dataQuality].[dbo].[dataCompleteness] A
    LEFT JOIN [dataQuality].[dbo].[markets] B
    ON A.[marketId]= B.[id]
    LEFT JOIN [dataQuality].[dbo].[universes] C
    ON A.[universeId]= C.[id]
    LEFT JOIN [dataQuality].[dbo].[presentationBlocks] D
    ON A.[presentationBlockId]= D.[id]
    ORDER BY A.[id]
    '''
data = readTable(query)

dash.register_page(__name__)

layout = layout = html.Div([
    html.H2(id='page_title', children='Data Quality Monitor'),
    html.Div([
    dcc.Dropdown(data.year.unique(),id = 'year', placeholder='Year...', className='dd2'),
    dcc.Dropdown(data.week.unique(),id = 'week', placeholder='Week...', className='dd2'),
    dcc.Dropdown(data.countryName.unique(),id = 'countryName', placeholder='country Name...', className='dd2'),
    dcc.Dropdown(data.universeDesc.unique(),id = 'universeDesc', placeholder='Universe...', className='dd3' ),
    html.Div([dbc.Button("SEARCH", id="data_quality_button", className="button2", n_clicks=0),]),
    html.Div([dcc.Loading(id="loading-1", children=[html.Div([html.Div(id="loading-output-1")])], type="circle",)],
              id="spinner", className="general-spinner"),
    ],id='options'),

	html.Div(children=[
    
        	html.Div(children=[
            	html.Div(children=[html.H3( id='basic_header', children=[html.Br(),'BASIC DATA'])], id='basic_header_div', className='section_header'),
                html.Div(children=[html.Br(),html.Br()], id='basic_chart_div'),
            ], id='basic_div'),
        	html.Div(children=[
            	html.Div(children=[html.H3( id='financia_header', children=[html.Br(),'FINANCIAL DATA'])], id='financia_header_div', className='section_header'),
                html.Div(children=[html.Br(),html.Br()], id='financial_chart_div'),
            ], id='financial_div'),
            html.Div(children=[
            	html.Div(children=[html.H3( id='shareholder_header', children=[html.Br(),'SHAREHOLDER DATA'])], id='shareholder_header_div', className='section_header'),
                html.Div(children=[html.Br(),html.Br()], id='shareholder_chart_div'),
            ], id='shareholders_div')

    ], id='data_div')
])

@callback(
    Output("loading-output-1", "children"),
    Output(component_id='basic_chart_div', component_property='children'),
    Output(component_id='financial_chart_div', component_property='children'),
    Output(component_id='shareholder_chart_div', component_property='children'),
    State(component_id='year', component_property='value'),
    State(component_id='week', component_property='value'),
    State(component_id='countryName', component_property='value'),
    State(component_id='universeDesc', component_property='value'),
    Input(component_id='data_quality_button', component_property='n_clicks'),
    prevent_initial_call=True
)

def get_dd2_content(year, week, countryName, universeDesc, n_clicks):

    
    if n_clicks == 0:
        raise PreventUpdate
    else:
        print(data)
        keys = list(locals().keys())
        values = list(locals().values())
        keys.pop()
        values.pop()

        vars = dict(zip(keys, values))
  
        for key, value in dict(vars).items():
            if value is None:
                del vars[key]

        filters=''

        for key, value in vars.items():
            if key == 'n_clicks':
                next

            elif type(value) == int :

                filters = filters + f'{key}=={value} and '

            else:
                filters = filters + f'{key}=="{value}" and '
        
        filters=filters[:-4]

        print(filters)

        if filters:

            filtered_data = data.query(filters)

        else:

            filtered_data = data

        sections =  filtered_data['desc'].unique()   

        print(sections)

        col_list = list()
        row_list = list()
        output_list = list()
        output_list.append(" READY ")

        col_count = 1
        progress_count = 1

        for item in sections:

            group_data = filtered_data.query(f'desc == "{item}"')
            values=group_data[['dataElement','rowsPopulated','rowsNonPopulated','rowsPopulatedPct','rowsNonPopulatedPct']]
            
            for row in values.itertuples():
                names =['Non populated', 'Populated']
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=[row.rowsPopulated],
                    orientation='h'))
                fig.add_trace(go.Bar(
                    x=[row.rowsNonPopulated],
                    orientation='h'))
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
                    paper_bgcolor='rgb(248, 248, 255)',
                    plot_bgcolor='rgb(248, 248, 255)',
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    width=100,
                    height=30
                )

                dbc_card  = dbc.Card([
                            dbc.CardHeader(html.Font(row.dataElement, className='card_title')),
                            dbc.CardBody([dcc.Graph(figure=fig, className='pie'),
                            # html.Div(children=[
                            #    dash_table.DataTable(row.to_dict('records'), [{"rowsPopulatedPct": i, "rowsNonPopulatedPct": i} for i in row.columns])

                            # ], id='card_content')
                            ]),
                            ],id=f'{row.dataElement}', className='card3')
            

                dbc_col =dbc.Col(dbc_card,width=1)
                col_list.append(dbc_col)
                if col_count == 10:
                    dbc_row = dbc.Row(col_list,className="g-1 dbc_row")
                    col_list = list()
                    row_list.append(dbc_row)
                    col_count = 0
                elif progress_count==len(group_data.index):
                    dbc_row = dbc.Row(col_list,className="g-1 dbc_row")
                    col_list = list()
                    row_list.append(dbc_row)

                col_count = col_count + 1
                progress_count = progress_count + 1

            output_list.append(row_list)

            col_count = 1
            progress_count = 1
            row_list = list()
            col_list = list()

    return output_list
