# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn import preprocessing



######################################################Data##############################################################
pd.set_option('mode.chained_assignment', None)

# DATA FRAMES PROCESSING:

df_football = pd.read_csv('DATABASE.csv')
CountryContinent = pd.read_csv("CountryContinent.csv", sep = ';')
transfers2 = df_football.merge(CountryContinent, how = 'left', left_on = 'Country_to', right_on = 'Country')
df_football['Country_to_B'] = df_football['Country_to']

for i in range(0,len(df_football['Country_to_B'])):
    if df_football['Country_to_B'][i] == 'England':
        df_football.at[i,'Country_to_B'] = 'United Kingdom'
    elif df_football['Country_to_B'][i] == 'Scotland':
        df_football.at[i,'Country_to_B'] = 'United Kingdom'
    elif df_football['Country_to_B'][i] == 'Wales':
        df_football.at[i,'Country_to_B'] = 'United Kingdom'

filtered_df_2 = df_football.groupby(['Country_to_B','Season']).agg(MoneySpent=('Transfer_fee', 'sum'), NumHires=('Transfer_fee', 'size')).reset_index()
filtered_df_2.rename(columns = {'Country_to_B' : 'Country'}, inplace = True)
filtered_df_2 = filtered_df_2.sort_values(['MoneySpent'], ascending=False)
filtered_df_2['Avg_TransferFee'] = filtered_df_2['MoneySpent']/filtered_df_2['NumHires']
filtered_df_2['Avg_TransferFee'] = filtered_df_2['Avg_TransferFee']

# FIRST PLOT
filtered_df = filtered_df_2[(filtered_df_2['Season'] == '2000-2001')]

layout_fig = dict(geo=dict(
        showframe=True,
        showcoastlines=False,
        landcolor='lightgreen',
        showocean=True,
        oceancolor='#e6e6e6',
        projection = dict(
            type='natural earth'
        ),
        bgcolor = '#e6e6e6',
    ),
        title=dict(text='Global View'),
        grid = dict(columns=1, rows=1),
        margin = dict(t=30, l=0, r=0, b=0),
        paper_bgcolor='#e6e6e6',
        plot_bgcolor='#e6e6e6',
)

data = [go.Choropleth(
            locationmode='country names',
            locations= filtered_df['Country'],
            z = filtered_df['Avg_TransferFee'],
            name = '',
            text = '<b>Country:</b> ' + filtered_df['Country'] +
                   '<br><b>Hires:</b> ' + filtered_df['NumHires'].astype(str) +
                   '<br><b>AVG Transfer Fee</b>: €'+ (filtered_df['Avg_TransferFee'].round(-5)/1000000).astype(str)+ 'M'+
                   '<br><b>Total Transfer Fee</b>: €' + (filtered_df['MoneySpent'].round(-5)/1000000).astype(str)+ 'M',
            hovertemplate= '%{text}',
            colorscale = 'blues',
            marker=go.choropleth.Marker(
                line=go.choropleth.marker.Line(
                    color='rgb(255,255,255)',
                    width=1
                )),
            colorbar=go.choropleth.ColorBar(title="AVG Transfers")
            )]

fig = go.Figure(data=data, layout=layout_fig)


# SECOND PLOT
df_football['Position_B'] = df_football['Position'].replace(to_replace={'Right Winger' : 'Winger',
                                                                    'Central Midfield' : 'Midfield',
                                                                    'Attacking Midfield' : 'Midfield',
                                                                    'Centre-Back' : 'Defender',
                                                                    'Left Midfield' : 'Midfield',
                                                                    'Right-Back' : 'Side Back',
                                                                    'Centre-Forward' : 'Forward',
                                                                    'Left-Back' : 'Side Back',
                                                                    'Defensive Midfield' : 'Midfield',
                                                                    'Second Striker' : 'Forward',
                                                                    'Goalkeeper' : 'Goalkeeper',
                                                                    'Right Midfield' : 'Midfield',
                                                                    'Left Winger' : 'Winger',
                                                                    'Forward' : 'Forward',
                                                                    'Sweeper' : 'Defender',
                                                                    'Defender' : 'Defender',
                                                                    'Midfielder' : 'Midfield'})

transfers2['Position_B'] = transfers2['Position'].replace(to_replace={'Right Winger' : 'Winger',
                                                                    'Central Midfield' : 'Midfield',
                                                                    'Attacking Midfield' : 'Midfield',
                                                                    'Centre-Back' : 'Defender',
                                                                    'Left Midfield' : 'Midfield',
                                                                    'Right-Back' : 'Side Back',
                                                                    'Centre-Forward' : 'Forward',
                                                                    'Left-Back' : 'Side Back',
                                                                    'Defensive Midfield' : 'Midfield',
                                                                    'Second Striker' : 'Forward',
                                                                    'Goalkeeper' : 'Goalkeeper',
                                                                    'Right Midfield' : 'Midfield',
                                                                    'Left Winger' : 'Winger',
                                                                    'Forward' : 'Forward',
                                                                    'Sweeper' : 'Defender',
                                                                    'Defender' : 'Defender',
                                                                    'Midfielder' : 'Midfield'})

Country = pd.DataFrame(df_football['Country_to'].append(df_football['Country_from']), columns = ["Country"]).drop_duplicates()
transfers = df_football.merge(CountryContinent, how = 'left', left_on = 'Country_to', right_on = 'Country')
transfers.drop(columns = ['Country'], inplace = True)

# transfers['Year'] = transfers['Season'].str[:4]
transfTeamSales = transfers.groupby(['Team_from','Country_from', 'Season']).agg(EarnedMoney=('Transfer_fee', 'sum'), NumSales=('Transfer_fee', 'size')).reset_index()
transfTeamPurchase = transfers.groupby(['Team_to','Country_to', 'Season']).agg(SpentMoney=('Transfer_fee', 'sum'), NumSignings=('Transfer_fee', 'size')).reset_index()
TransfTeam = transfTeamSales.merge(transfTeamPurchase, left_on = ['Country_from', 'Team_from', 'Season'], right_on = ['Country_to', 'Team_to', 'Season'], how = 'outer' )
TransfTeam.loc[TransfTeam['Team_from'].isna(), 'Team_from'] = TransfTeam['Team_to']
TransfTeam.loc[TransfTeam['Country_from'].isna(), 'Country_from'] = TransfTeam['Country_to']
TransfTeam.drop(columns = ['Team_to', 'Country_to'], inplace = True)
TransfTeam.fillna(0, inplace = True)
TransfTeam.rename(columns = {'Team_from' : 'Team', 'Country_from' : 'Country'}, inplace = True)
data_2 = TransfTeam.loc[TransfTeam["Season"] == '2000-2001']
data_2 = data_2.sort_values(['Country'])
Country_names = data_2['Country'].unique()
Country_data = {Country: data_2.query("Country == '%s'" % Country)
                for Country in Country_names}

data2 = [go.Scatter(
        type='scatter',
        x=Country['EarnedMoney'],
        y=Country['SpentMoney'],
        name=Country_names,
        text=Country['Team'],
        hovertemplate=
        '<b>%{text}</b>' +
        '<br><b>Spending</b>: €%{y}' +
        '<br><b>Earnings</b>: €%{x}' +
        '<br><b>Transfers</b>: %{marker.size:}',
        mode='markers',
        marker=dict(size=Country['NumSignings']+Country['NumSales'],
                    sizeref=0.3)
)for Country_names, Country in Country_data.items()]

layout_fig2 = dict(title='Total Transfers Per Team',
                   xaxis=dict(title='Total Recived by Sales'),
                   yaxis=dict(title='Total Invested in Hiring'),
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   grid=dict(columns=1, rows=1),
                   margin=dict(t=30, l=0, r=0, b=0),
                   )

fig2 = go.Figure(data=data2, layout=layout_fig2)

# THIRD PLOT
Sunburst_df = transfers2.loc[transfers2["Season"] == '2000-2001']
columnSet = ['Season', 'Continent', 'Country_to', 'Team_to', 'Position_B', 'Name']
database = pd.DataFrame(columns= ['ids', 'labels', 'parents', 'transfers', 'transferfee'])
for i, columnName in enumerate(columnSet):
    database1 = pd.DataFrame(columns= ['ids', 'labels', 'parents', 'transfers', 'transferfee'])
    groupdf = Sunburst_df.groupby(columnSet[:i+1]).agg(transfers = ('Transfer_fee', 'size'), transferfee = ('Transfer_fee', 'sum')).reset_index()
    if i == 0:
        database1['ids'] = groupdf[columnName]
        database1['labels'] = groupdf[columnName]
        database1['transfers'] = groupdf['transfers']
        database1['transferfee'] = groupdf['transferfee']
        database = database.append(database1)
    else:
        groupdf['combined1'] = groupdf[columnSet[:i+1]].apply(lambda row: ' - '.join(row.values.astype(str)), axis=1)
        groupdf['combined2'] = groupdf[columnSet[:i]].apply(lambda row: ' - '.join(row.values.astype(str)), axis=1)
        database1['ids'] = groupdf['combined1']
        database1['labels'] = groupdf[columnName]
        database1['parents'] = groupdf['combined2']
        database1['transfers'] = groupdf['transfers']
        database1['transferfee'] = groupdf['transferfee']
        database = database.append(database1)

data3 = go.Sunburst(
    ids=database.ids,
    labels=database.labels,
    parents=database.parents,
    values=database.transfers,
    branchvalues = 'total',
    name='Investments',
    marker=dict(
        cmin=transfers['Transfer_fee'].min(),
        cmax=transfers['Transfer_fee'].quantile(.999),
        colors=database.transferfee,
        colorscale='blues',
        line=dict(color='darkgrey')),
    hovertemplate='<b>%{label} </b> <br> Transfers: %{value}<br> Transfer fee: €%{color:,}',
    maxdepth=3,
)

layout_fig3 = dict(title = 'Purchase Map',
    grid= dict(columns=1, rows=1),
    margin = dict(t=65, l=0, r=0, b=50),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig3 = go.Figure(data=data3, layout=layout_fig3)

# FORTH PLOT
transfSeasonSales = transfers.groupby(['Country_to','Team_to','Season']).agg(MoneySpent=('Transfer_fee', 'sum'), NumHires=('Transfer_fee', 'size')).reset_index()
transfSeasonSales.rename(columns = {'Team_to' : 'Team', 'Country_to' : 'Country'}, inplace = True)
transfSeasonSales = transfSeasonSales.sort_values(['Season', 'MoneySpent'])
transfSeasonSales['Season_Ranking'] =  transfSeasonSales.groupby('Season')['MoneySpent'].rank(method = 'first', ascending=False)
transfSeasonSales['Season_Ranking'] = transfSeasonSales['Season_Ranking'].astype(int)

MinSeasonSale = transfers.sort_values(['Season','Transfer_fee'])
MinSeasonSale.drop_duplicates(subset=['Season'], keep='first', inplace=True)
MinSeasonSale['Age']=MinSeasonSale['Age'].apply(str)
MaxSeasonSale = transfers.sort_values(['Season','Transfer_fee'])
MaxSeasonSale.drop_duplicates(subset=['Season'], keep='last', inplace=True)
MaxSeasonSale['Age']=MaxSeasonSale['Age'].apply(str)

fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4 = go.Figure(data = fig4.add_trace(go.Bar(x=transfSeasonSales['Season'] ,
                     y=transfSeasonSales['MoneySpent'],
                     name="Amount Spend by Team",
                     text=transfSeasonSales['Team']+ ' - ' +transfSeasonSales['Country'],
                     hovertemplate='<b>%{text}</b>' +
                                   '<br><b>Spending</b>: €%{y}',
                     marker_color='dimgray')
                     ,secondary_y=False,))
fig4 = go.Figure(data = fig4.add_trace(go.Scatter(x=MaxSeasonSale['Season'],
                         y=MaxSeasonSale['Transfer_fee'],
                        name="Highest Transfer",
                        text="Player: "+MaxSeasonSale['Name'] + ' ('+MaxSeasonSale['Age'] +"yrs) <br>"+
                             "From: "+MaxSeasonSale['Team_from']+" - "+MaxSeasonSale['Country_from']+" <br>"+
                             "To: "+MaxSeasonSale['Team_to']+" - "+MaxSeasonSale['Country_to'],
                        hovertemplate= '%{text}' +
                                       '<br><b>Transfer fee</b>: €%{y}',
                              marker_color='navy'
                        ),secondary_y=True))
fig4 = go.Figure(data = fig4.add_trace(go.Scatter(x=MinSeasonSale['Season'],
                         y=MinSeasonSale['Transfer_fee'],
                        name="Lowest Transfer",
                        text="Player: "+MinSeasonSale['Name'] + ' ('+MinSeasonSale['Age'] +"yrs) <br>"+
                             "From: "+MinSeasonSale['Team_from']+" - "+MinSeasonSale['Country_from']+" <br>"+
                             "To: "+MinSeasonSale['Team_to']+" - "+MinSeasonSale['Country_to'],
                        hovertemplate= '%{text}' +
                                       '<br><b>Transfer fee</b>: €%{y}',
                         marker_color='red'
                        ),secondary_y=True))

fig4.update_layout(dict(title = 'Total Transfers by Team per Season',
                       xaxis = dict(title = 'Season'),
                       yaxis = dict(title = 'Transfer Fee Team'),
                       legend= dict(x=-.1, y=1.1),
                       legend_orientation="h"),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        grid= dict(columns=1, rows=1),
                        margin = dict(t=80, l=0, r=0, b=0),
)

fig4.update_yaxes(title_text="Highest\Lowest Transfer Fee ", secondary_y=True)

# FIFTH PLOT
CountryRelations = transfers.groupby(['Country_to','Country_from', 'Season']).agg(Transfer_fee=('Transfer_fee', 'sum'), Transactions = ('Transfer_fee', 'size')).reset_index()

Country = pd.DataFrame(CountryRelations['Country_to'].append(CountryRelations['Country_from']), columns = ["Country"])
Country.drop_duplicates(inplace=True)

le = preprocessing.LabelEncoder()
Country["Country_ind"] = le.fit_transform(Country["Country"])
Country.sort_values(['Country_ind'], inplace = True)
CountryRelations = CountryRelations.merge(Country, how = 'left', left_on = 'Country_to', right_on = 'Country')
CountryRelations = CountryRelations.merge(Country, how = 'left', left_on = 'Country_from', right_on = 'Country')
CountryRelations.sort_values(['Transfer_fee'], inplace = True, ascending=False)
CountryRelations2 = CountryRelations.loc[CountryRelations['Season'] == '2000-2001']
CountryRelations2 = CountryRelations2.iloc[0:50]

data5 = go.Sankey(
    valuesuffix="€",

    # Define nodes
    node=dict(label=Country["Country"]

              ),
    # Add links
    link=dict(
        source=CountryRelations2["Country_ind_y"],
        target=CountryRelations2["Country_ind_x"],
        value=CountryRelations2["Transfer_fee"],
        label='<b>' + CountryRelations2["Country_y"] + '</b>' + ' To ' + '<b>' + CountryRelations[
            "Country_x"] + '</b>' + '<br>' +
              '<b>Transfers:</b> ' + CountryRelations2["Transactions"].astype(str),
        hovertemplate='%{label}'
    ))

layout_fig5 = dict(title = 'Top 50 Relations between Countries',
    grid= dict(columns=1, rows=1),
    margin = dict(t=65, l=50, r=0, b=0),
    paper_bgcolor= '#e6e6e6',
    plot_bgcolor='rgba(0,0,0,0)',
)

fig5 = go.Figure(data=data5, layout = layout_fig5)

# SIXTH PLOT
CountryRelations_b = CountryRelations2.iloc[:20]
CountryRelations_b['Relations'] = (CountryRelations_b['Country_from'] + ' to '+ CountryRelations_b['Country_to'])
CountryRelations_b['Transfer_fee'] = CountryRelations_b['Transfer_fee'].astype(int)
CountryRelations_b.sort_values(['Transfer_fee'], inplace = True, ascending = False)

data6 = go.Table(columnwidth = [6,3,1],
                header=dict(values=['<b>Trades between<br>Countries.</b> From-To',
                                    '<b>Transfer</b><br> in MM.€', '<b>Nº</b><br>'],
                                           align=['center','center','center'],
                                            fill = dict(color = 'midnightblue'),
                                            font = dict(color = 'white')),
                               cells=dict(values=[CountryRelations_b['Relations'],
                                                  (CountryRelations_b['Transfer_fee']/1000000).round(1),
                                                  CountryRelations_b['Transactions']],
                                                  line = dict(color = 'black'),
                                                  fill = dict(color='#e6e6e6'),
                                                  font = dict(color='black'))
                )

layout_fig6 = dict(
    grid= dict(columns=1, rows=1),
    margin = dict(t=0, l=0, r=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig6 = go.Figure(data = data6, layout = layout_fig6)

##################################################APP###############################################################

app = dash.Dash(__name__)
server = app.server

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div([
                    html.Img(src='assets/image.png')
                ],style={"margin-left": "115px"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Football Manager",
                                    style={"margin-bottom": "0px","margin-right": "400px"},
                                ),
                                html.H5(
                                    "Transfers Dashboard", style={"margin-top": "0px","margin-right": "400px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.P("Choose a season:", className="control_label"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[{'label' : '2000-2001', 'value' : '2000-2001' },
                             {'label' : '2001-2002', 'value' : '2001-2002' },
                             {'label' : '2002-2003', 'value' : '2002-2003' },
                             {'label' : '2003-2004', 'value' : '2003-2004' },
                             {'label' : '2004-2005', 'value' : '2004-2005' },
                             {'label' : '2005-2006', 'value' : '2005-2006' },
                             {'label' : '2006-2007', 'value' : '2006-2007' },
                             {'label' : '2007-2008', 'value' : '2007-2008' },
                             {'label' : '2008-2009', 'value' : '2008-2009' },
                             {'label' : '2009-2010', 'value' : '2009-2010' },
                             {'label' : '2011-2012', 'value' : '2011-2012' },
                             {'label' : '2012-2013', 'value' : '2012-2013' },
                             {'label' : '2013-2014', 'value' : '2013-2014' },
                             {'label' : '2014-2015', 'value' : '2014-2015' },
                             {'label' : '2015-2016', 'value' : '2015-2016' },
                             {'label' : '2016-2017', 'value' : '2016-2017' },
                             {'label' : '2017-2018', 'value' : '2017-2018' },
                        ],
                        value='2000-2001'
                        ),
                    ],className="pretty_container three columns",id="cross-filter-options",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div([dcc.Graph(id='graph3-with-slider')],
                                     className="pretty_container three columns",
                ),
                html.Div([dcc.Graph(id='graph5-with-slider')],
                                     className="pretty_container seven columns",
                ),
                html.Div([dcc.Graph(id='graph6-with-slider')],
                                    className="pretty_container three columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.Div([dcc.Graph(id='graph-with-slider')])],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.Div([dcc.Graph(id='graph2-with-slider')])],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div([
            html.Div(
                [dcc.Graph(id='graph4-with-slider', figure=fig4)
                ], className="pretty_container2 twelve columns",
            ),
        ],className="row flex-display")
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-dropdown', 'value')])

def update_figure1(selected_year):
    filtered_df = filtered_df_2.loc[filtered_df_2['Season'] == selected_year]

    data = [go.Choropleth(
        locationmode='country names',
        locations=filtered_df['Country'],
        z=filtered_df['Avg_TransferFee'],
        name='',
        text='<b>Country:</b> ' + filtered_df['Country'] +
             '<br><b>Hires:</b> ' + filtered_df['NumHires'].astype(str) +
             '<br><b>AVG Transfer Fee</b>: €' + (filtered_df['Avg_TransferFee'].round(-5) / 1000000).astype(str) + 'M' +
             '<br><b>Total Transfer Fee</b>: €' + (filtered_df['MoneySpent'].round(-5) / 1000000).astype(str) + 'M',
        hovertemplate='%{text}',
        colorscale='blues',
        marker=go.choropleth.Marker(
            line=go.choropleth.marker.Line(
                color='rgb(255,255,255)',
                width=1
            )),
        colorbar=go.choropleth.ColorBar(title="AVG Transfers")
    )]

    return go.Figure(data=data, layout=layout_fig)

@app.callback(
    Output('graph2-with-slider', 'figure'),
    [Input('year-dropdown', 'value')])

def update_figure2(selected_year):
    data_2 = TransfTeam.loc[TransfTeam["Season"] == selected_year]
    data_2 = data_2.sort_values(['Country'])
    Country_names = data_2['Country'].unique()
    Country_data = {Country: data_2.query("Country == '%s'" % Country)
                    for Country in Country_names}

    data2 = [go.Scatter(
                type='scatter',
                x=Country['EarnedMoney'],
                y=Country['SpentMoney'],
                name=Country_names,
                text=Country['Team'],
                hovertemplate=
                '<b>%{text}</b>' +
                '<br><b>Spending</b>: €%{y}' +
                '<br><b>Earnings</b>: €%{x}' +
                '<br><b>Transfers</b>: %{marker.size:}',
                mode='markers',
                marker=dict(size=Country['NumSignings'] + Country['NumSales'],
                    sizeref=0.3)

        ) for Country_names, Country in Country_data.items()]

    return go.Figure(data=data2, layout=layout_fig2)


@app.callback(
    Output('graph3-with-slider', 'figure'),
    [Input('year-dropdown', 'value')])

def update_figure3(selected_year):
    Sunburst_df = transfers2.loc[transfers2["Season"] == selected_year]

    columnSet = ['Season', 'Continent', 'Country_to', 'Team_to', 'Position_B', 'Name']
    database = pd.DataFrame(columns=['ids', 'labels', 'parents', 'transfers', 'transferfee'])
    for i, columnName in enumerate(columnSet):
        database1 = pd.DataFrame(columns=['ids', 'labels', 'parents', 'transfers', 'transferfee'])
        groupdf = Sunburst_df.groupby(columnSet[:i + 1]).agg(transfers=('Transfer_fee', 'size'),
                                                             transferfee=('Transfer_fee', 'sum')).reset_index()
        if i == 0:
            database1['ids'] = groupdf[columnName]
            database1['labels'] = groupdf[columnName]
            database1['transfers'] = groupdf['transfers']
            database1['transferfee'] = groupdf['transferfee']
            database = database.append(database1)
        else:
            groupdf['combined1'] = groupdf[columnSet[:i + 1]].apply(lambda row: ' - '.join(row.values.astype(str)),
                                                                    axis=1)
            groupdf['combined2'] = groupdf[columnSet[:i]].apply(lambda row: ' - '.join(row.values.astype(str)), axis=1)
            database1['ids'] = groupdf['combined1']
            database1['labels'] = groupdf[columnName]
            database1['parents'] = groupdf['combined2']
            database1['transfers'] = groupdf['transfers']
            database1['transferfee'] = groupdf['transferfee']
            database = database.append(database1)

    data3 = go.Sunburst(
        ids=database.ids,
        labels=database.labels,
        parents=database.parents,
        values=database.transfers,
        branchvalues='total',
        name='Investments',
        marker=dict(
            cmin=transfers['Transfer_fee'].min(),
            cmax=transfers['Transfer_fee'].quantile(.999),
            colors=database.transferfee,
            colorscale='blues',
            line=dict(color='darkgrey')),
        hovertemplate='<b>%{label} </b> <br> Transfers: %{value}<br> Transfer fee: €%{color:,}',
        maxdepth=3
    )

    return go.Figure(data=data3, layout=layout_fig3)

@app.callback(
    Output('graph5-with-slider', 'figure'),
    [Input('year-dropdown', 'value')])


def update_figure4(selected_year):

    CountryRelations2 = CountryRelations.loc[CountryRelations['Season'] == str(selected_year)]
    CountryRelations2 = CountryRelations2.iloc[0:50]

    data5 = go.Sankey(
        valuesuffix="€",

        # Define nodes
        node=dict(label=Country["Country"]

                  ),
        # Add links
        link=dict(
            source=CountryRelations2["Country_ind_y"],
            target=CountryRelations2["Country_ind_x"],
            value=CountryRelations2["Transfer_fee"],
            label='<b>' + CountryRelations2["Country_y"] + '</b>' + ' To ' + '<b>' + CountryRelations2[
                "Country_x"] + '</b>' + '<br>' +
                  '<b>Transfers:</b> ' + CountryRelations2["Transactions"].astype(str),
            hovertemplate='%{label}'
        ))

    return go.Figure(data=data5, layout = layout_fig5)

@app.callback(
    Output('graph6-with-slider', 'figure'),
    [Input('year-dropdown', 'value')])

def update_figure5(selected_year):
    CountryRelations2 = CountryRelations.loc[CountryRelations['Season'] == str(selected_year)]

    CountryRelations_b = CountryRelations2.iloc[:20]
    CountryRelations_b['Relations'] = (CountryRelations_b['Country_from'] + ' to '+ CountryRelations_b['Country_to'])
    CountryRelations_b['Transfer_fee'] = CountryRelations_b['Transfer_fee'].astype(int)
    CountryRelations_b.sort_values(['Transfer_fee'], inplace=True, ascending=False)

    data6 = go.Table(columnwidth=[6, 3, 1],
                     header=dict(values=['<b>Trades between<br>Countries.</b> From-To',
                                         '<b>Transfer</b><br> in MM.€', '<b>Nº</b><br>'],
                                 align=['center', 'center', 'center'],
                                 fill=dict(color='midnightblue'),
                                 font=dict(color='white')),
                     cells=dict(values=[CountryRelations_b['Relations'],
                                        (CountryRelations_b['Transfer_fee'] / 1000000).round(1),
                                        CountryRelations_b['Transactions']],
                                line=dict(color='black'),
                                fill=dict(color='#e6e6e6'),
                                font=dict(color='black'))
                      )

    return go.Figure(data = data6, layout = layout_fig6)

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
