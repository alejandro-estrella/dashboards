import dash
import os
from dash import html, dcc, callback, Input, Output
from dash.dependencies import State
import pandas as pd
from dash.dependencies import Input, Output
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import text
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
from dash.exceptions import PreventUpdate

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

host = (os.environ.get('SQLHOST'))
print(host)
username = (os.environ.get('SQLUSER'))
password = (os.environ.get('SQLPASS'))
connection_url = URL.create("mssql+pymssql", username=username, password=password, host=host, database='ticketsData')
dbEngine = create_engine(connection_url)

# host = 'NJ-SQL001.cialdnb.com'
# username = 'tickets'
# password = 'Eega690804666'
# connection_url = URL.create("mssql+pymssql", username=username, password=password, host=host, database='ticketsData')
# dbEngine = create_engine(connection_url)

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
            

query = 'SELECT  FROM mexico WHERE [AssignedTo] IS NOT NULL'

analyst_output = readColumn(db, query, 'AssignedTo')

analyst_list = analyst_output['AssignedTo'].to_list()

dash.register_page(__name__)

layout = html.Div(children=[
    html.H2(id='page_title', children='2022 TICKET DATA'),
	html.Div([

    dcc.Dropdown(id = 'analyst-dd', placeholder='Analyst name...', className='dd', options=[
            {'label': i, 'value': i} for i in analyst_list
            ]),
    dcc.Dropdown(id = 'task-dd', placeholder='Task name...', className='dd', options=[
            {'label': '', 'value': ''}
            ]),
    html.Div([dbc.Button("Run", id="apply-button", className="me-2", n_clicks=0),]),
    ],id='options'),
	html.Br(),
    html.Div(children=[
        html.Div( children=[
            html.Div(children=[
                dcc.Graph(id='timeline',className= 'grph1', figure={'data': []}),
            ],id='SQL1'),
            html.Div(children=[
                dcc.Graph(id='histogram',className= 'grph2', figure={'data': []}),
            ],id='SQL2'),
            html.Div(children=[
                dcc.Graph(id='density',className= 'grph3', figure={'data': []}),
            ],id='SQL3')

        ],id='wrapper2')
    ],id='SQL-output'),
],id='main')

@callback(
    Output(component_id='task-dd', component_property='options'),
    Input(component_id='analyst-dd', component_property='value'),
    prevent_initial_call=True
)

def get_dd2_content(value):
    sql = f'''
        SELECT DISTINCT [TaskName] FROM [ticketsData].[dbo].[mexico]
        WHERE [AssignedTo]='{value}'
    '''
    task_data = readColumn(db, sql, 'AssignedTo')
    task_data_list = task_data['AssignedTo'].to_list()
    task_list = []
    for task in task_data_list:
        dd = {'label': task, 'value': task} 
        task_list.append(dd)

    return task_list

@callback(
    Output(component_id='timeline', component_property='figure'),
    Output(component_id='histogram', component_property='figure'),
    Output(component_id='density', component_property='figure'),
    Output(component_id='apply-button', component_property='n_clicks'),
    State(component_id='task-dd', component_property='value'),
    State(component_id='analyst-dd', component_property='value'),
    Input(component_id='apply-button', component_property='n_clicks'),
    prevent_initial_call=True
)

def get_dd1_content(task_dd, analyst_dd, n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        sql = f'''
        SELECT [InvestKey]
            ,[CaseReceivedDate]
            ,[CaseCompletionDate]
            ,[AssignedTo]
            ,[AssignedDate]
            ,[step_duration]
            ,[duration]
        FROM [ticketsData].[dbo].[mexico]
        WHERE [AssignedTo]='{analyst_dd}' AND [TaskName]='{task_dd}'
        '''
        analyst_data = readTable(db, sql)

        analyst_data['CaseReceivedDate']=analyst_data['CaseReceivedDate'].dt.strftime('%Y/%m/%d %H:%M:%S')
        analyst_data['CaseCompletionDate']=analyst_data['CaseCompletionDate'].dt.strftime('%Y/%m/%d %H:%M:%S')

        analyst_data['duration'] = analyst_data['duration'].div(86400)

        resampled = analyst_data[['AssignedDate','duration','CaseReceivedDate','CaseCompletionDate']]
        resampled = resampled.sort_values(by=['AssignedDate'])
        resampled = resampled.set_index('AssignedDate')
        resampled['duration']= resampled['duration'].round(2)
        
        fig1 = px.scatter(resampled, x=resampled.index, y='duration', color="duration", hover_data=['CaseReceivedDate', 'CaseCompletionDate', 'duration'], color_continuous_scale=['lime','yellow','red'])
        fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        fig1.update_xaxes(tickformat="%Y/%m/%d")
        fig1.update_traces(marker=dict(size=7, line=dict(width=1)),selector=dict(mode='markers'))

        fig2 = px.histogram(analyst_data['duration'], x='duration', labels={'x':'Task Duration', 'y':'Count'})
        fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        group_labels = ['distplot']

        fig3 = ff.create_distplot([analyst_data['duration'].to_numpy()], group_labels, show_hist=False)
        fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=False)

        return [fig1, fig2, fig3, 0]

