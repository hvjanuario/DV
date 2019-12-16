#from datetime import datetime as dt
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go


######################################################Data##############################################################

df = pd.read_csv('data/top250Transfers.txt', sep=',', header=0)
df1 = pd.read_csv('data/TeamLeagueCountry.csv', sep=';',header=0)
df.columns = ['ID', 'Name', 'Position', 'Age', 'Team_from', 'League_from', 'Team_to',
              'League_to', 'Season', 'Market_value', 'Transfer_fee', 'Country_from', 'Country_to']





######################################################Interactive Components############################################

country_options = [dict(label=country, value=country)
                   for country in df['Country_from'].unique()]

team_options = [dict(label=team, value=team)
               for team in df['Team_from'].unique()]

league_options = [dict(label=league, value=league)
               for league in df['League_from'].unique()]

######################################################APP###############################################################

app = dash.Dash(__name__)
app.layout = html.Div([

                html.Div([
                    html.H1('Project Title')
                ], classname='row1'),

                html.Div([
                    html.Div([],classname='')

                ], classname='row2')

            ])

app = dash.Dash(__name__)
app.layout = html.Div([
                #title area
                html.Div([
                    html.H1('Project Title')
                ], className='row1'),

                html.Div([
                    html.Div([
                        html.Div([],className=''),
                        html.Div([],className=''),
                        html.Div([],className='')
                    ], className='col_side'), #put selectors here

                    html.Div([
                        html.Div([
                            html.Div([], className='col3'),
                            html.Div([], className='col3'),
                            html.Div([], className='col3'),
                            html.Div([], className='col3'),
                            html.Div([], className='col3')

                        ], className=' row_1'),

                        html.Div([], className='pretty')

                    ], className=' col2')
                ], className='row2'),

            ])

######################################################Callbacks#########################################################


@app.callback(
    [


    ]
)

    ############################################First Bar Plot##########################################################


    #############################################Second Choropleth######################################################


    ############################################Third Scatter Plot######################################################


@app.callback(
    [

    ],
    [

    ]
)


######################################################Run the app#######################################################
if __name__ == '__main__':
    app.run_server(debug=True)







