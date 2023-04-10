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
            

query = '''SELECT DISTINCT B.[countryName]
  FROM [cherishedUniverse].[dbo].[cherishedUniverseAttributes] AS A
  LEFT JOIN [cherishedUniverse].[dbo].[countries] AS B
  ON A.[countryId] = B.id'''

countries = readTable(db, query)

country_list = countries['countryName'].to_list()

dash.register_page(__name__)

layout = html.Div(children=[
    html.H2(id='page_title', children='Cherished UNiverse Analysis & Follow uP'),
	html.Div([

    dcc.Dropdown(id = 'country-dd', placeholder='Country name...', className='dd', options=[
            {'label': i, 'value': i} for i in country_list
            ])
    ],id='SQL-output'),
],id='main')

