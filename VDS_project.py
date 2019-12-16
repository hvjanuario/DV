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

### Option 1 (class one)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Emissions Title')

    ], className='container row 1'),

    html.Div([

        html.Div([

            #left hand side little selector box

        ], className='pretty container col1'),

        html.Div([
            html.Div([
                #little boxes up top
                html.Div([], className='pretty col3'),
                html.Div([], className='pretty col3'),
                html.Div([], className='pretty col3'),
                html.Div([], className='pretty col3'),
                html.Div([], className='pretty col3')

            ], className=' row 1'),

            html.Div([

                #first graph

            ], className='pretty')

        ], className=' col2')

    ], className=' row 2'),

    html.Div([
        #last row of graphs
        html.Div([], className='pretty column'),

        html.Div([], className='pretty column')

    ], className=' row 3')
])




#Option 2 (uber rides thing)
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("DASH - UBER DATA APP"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different time frames on the histogram."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2014, 4, 1),
                                    max_date_allowed=dt(2014, 9, 30),
                                    initial_visible_month=dt(2014, 4, 1),
                                    date=dt(2014, 4, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

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







