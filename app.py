import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
from sklearn import preprocessing


# DATA FRAMES PROCESSING:

df_football = pd.read_csv('DATABASE.csv')
CountryContinent = pd.read_csv("CountryContinent.csv", sep = ';')
partial = df_football[(df_football['Year'] == 2000)]

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


Country = pd.DataFrame(df_football['Country_to'].append(df_football['Country_from']), columns = ["Country"]).drop_duplicates()

transfers = df_football.merge(CountryContinent, how = 'left', left_on = 'Country_to', right_on = 'Country')

transfers.drop(columns = ['Country'], inplace = True)
transfers.head()


transfers['Year'] = transfers['Season'].str[:4]
transfTeamSales = transfers.groupby(['Team_from','Country_from', 'Year']).agg(EarnedMoney=('Transfer_fee', 'sum'), NumSales=('Transfer_fee', 'size')).reset_index()
transfTeamPurchase = transfers.groupby(['Team_to','Country_to', 'Year']).agg(SpentMoney=('Transfer_fee', 'sum'), NumSignings=('Transfer_fee', 'size')).reset_index()
TransfTeam = transfTeamSales.merge(transfTeamPurchase, left_on = ['Country_from', 'Team_from', 'Year'], right_on = ['Country_to', 'Team_to', 'Year'], how = 'outer' )
TransfTeam.loc[TransfTeam['Team_from'].isna(), 'Team_from'] = TransfTeam['Team_to']
TransfTeam.loc[TransfTeam['Country_from'].isna(), 'Country_from'] = TransfTeam['Country_to']
TransfTeam.drop(columns = ['Team_to', 'Country_to'], inplace = True)
TransfTeam.fillna(0, inplace = True)
TransfTeam.rename(columns = {'Team_from' : 'Team', 'Country_from' : 'Country'}, inplace = True)
data_2 = TransfTeam.loc[TransfTeam["Year"] == '2000']
data_2 = data_2.sort_values(['Country'])
Country_names = data_2['Country'].unique()
Country_data = {Country: data_2.query("Country == '%s'" % Country)
                for Country in Country_names}

data=[go.Choropleth(
    locationmode='country names',
    locations=partial.loc[partial['Country_from'] == i]['Country_from'].unique(),
    z=[partial.loc[partial['Country_from'] == i]['Transfer_fee'].sum()],
    text=[partial.loc[partial['Country_from'] == i]['Name'].to_string()],
    colorscale = [
        [0, "rgb(5, 10, 172)"],
        [0.35, "rgb(40, 60, 190)"],
        [0.5, "rgb(70, 100, 245)"],
        [0.6, "rgb(90, 120, 245)"],
        [0.7, "rgb(106, 137, 247)"],
        [1, "rgb(220, 220, 220)"]
    ],
    colorbar_title='Football',
) for i in partial['Country_from'].unique()]

layout_fig = dict(geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
        height=600,
        title=dict(text='Football'),
        )

fig = go.Figure(data=data, layout=layout_fig)

# SECOND PLOT
transfers = transfers.sort_values(['Age'])
Age_yrs = transfers['Age'].unique()
Age_data = {Age :transfers.query("Age == '%s'" %Age)
                              for Age in Age_yrs}


# THIRD PLOT
transfSeasonSales = transfers.groupby(['Country_to','Team_to','Season']).agg(MoneySpent=('Transfer_fee', 'sum'), NumHires=('Transfer_fee', 'size')).reset_index()
transfSeasonSales.rename(columns = {'Team_to' : 'Team', 'Country_to' : 'Country'}, inplace = True)
transfSeasonSales = transfSeasonSales.sort_values(['Season', 'MoneySpent'])

MinSeasonSale = transfers.sort_values(['Season','Transfer_fee'])
MinSeasonSale.drop_duplicates(subset=['Season'], keep='first', inplace=True)
MinSeasonSale['Age']=MinSeasonSale['Age'].apply(str)
MaxSeasonSale = transfers.sort_values(['Season','Transfer_fee'])
MaxSeasonSale.drop_duplicates(subset=['Season'], keep='last', inplace=True)
MaxSeasonSale['Age']=MaxSeasonSale['Age'].apply(str)

# FOURTH PLOT

CountryRelations = transfers.groupby(['Country_to','Country_from']).agg(Transfer_fee=('Transfer_fee', 'sum'), Transactions = ('Transfer_fee', 'size')).reset_index()
#CountryRelations = CountryRelations[CountryRelations['Country_to'] != CountryRelations['Country_from']]

Country = pd.DataFrame(CountryRelations['Country_to'].append(CountryRelations['Country_from']), columns = ["Country"])
Country.drop_duplicates(inplace=True)

le = preprocessing.LabelEncoder()
Country["Country_ind"] = le.fit_transform(Country["Country"])
Country.sort_values(['Country_ind'], inplace = True)
CountryRelations = CountryRelations.merge(Country, how = 'left', left_on = 'Country_to', right_on = 'Country')
CountryRelations = CountryRelations.merge(Country, how = 'left', left_on = 'Country_from', right_on = 'Country')
CountryRelations.sort_values(['Transfer_fee'], inplace = True, ascending=False)
CountryRelations = CountryRelations.head(50)

# FIFTH PLOT
columnSet = ['Continent', 'Country_to', 'Team_to', 'Position_B', 'Name']
database = pd.DataFrame(columns= ['ids', 'labels', 'parents', 'transfers', 'transferfee'])
for i, columnName in enumerate(columnSet):
    database1 = pd.DataFrame(columns= ['ids', 'labels', 'parents', 'transfers', 'transferfee'])
    groupdf = transfers.groupby(columnSet[:i+1]).agg(transfers = ('Transfer_fee', 'size'), transferfee =  ('Transfer_fee', 'sum')).reset_index()
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

fee_max = 30

#FIRST PLOT

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
        '<br><b>Sales</b>: %{marker.size:}',
        mode='markers',
        marker=dict(size=Country['NumSignings'],
                    sizeref=2)
)for Country_names, Country in Country_data.items()]

layout_fig2 = dict(title='Total Transfers Per Team 2000 - 2019',
                   xaxis=dict(title='Total Recived by Sales'),
                   yaxis=dict(title='Total Invested in Hiring'))

fig2 = go.Figure(data=data2, layout=layout_fig2)

# SECOND PLOT
fig3 = go.Figure()

for Age_yrs, Age in Age_data.items():
    fig3 = go.Figure(data = fig3.add_trace(go.Scatter(
            type='scatter',
            x=Age['Transfer_fee'],
            y=Age['Position_B'],
            name=str(Age_yrs),
            text=Age['Name'],
            hovertemplate=
            '<b>%{text}</b>' +
            '<br><b>Spending</b>: €%{y}' +
            '<br><b>Earnings</b>: €%{x}' +
            '<br><b>Sales</b>: %{marker.size:}',
            mode='markers',
            # marker = dict(size = Position['NumSignings'],
            #              sizeref = 2)
            )))

fig3.update_layout(dict(title='Total Transfers Per Team 2000 - 2019',
                       xaxis=dict(title='Total Recived by Sales'),
                       yaxis=dict(title='Total Invested in Hiring')))

# THIRD PLOT
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
                       legend_orientation="h"))

fig4.update_yaxes(title_text="Highest\Lowest Transfer Fee ", secondary_y=True)


# FOURTH PLOT

fig5 = go.Figure(data = go.Sankey(
    valuesuffix = "€",
    # Define nodes
    node = dict(label = Country["Country"]
               ),
    # Add links
    link = dict(
          source =  CountryRelations["Country_ind_y"],
          target =  CountryRelations["Country_ind_x"],
          value =   CountryRelations["Transfer_fee"],
          hovertemplate = '%{x}' + '<br><b>Transfer fee</b>: €%{y}'
      )))

# FIFTH PLOT

fig6 = go.Figure()

fig6 = go.Figure(data = fig6.add_trace(go.Sunburst(
    ids=database.ids,
    labels=database.labels,
    parents=database.parents,
    values=database.transfers,
    branchvalues = 'total',
    marker=dict(
        cmin = transfers['Transfer_fee'].min(),
        cmax = 1820000000,
        colors=database.transferfee,
        colorscale='OrRd'),
    hovertemplate='<b>%{label} </b> <br> Transfers: %{value}<br> Transfer fee: €%{color:,}',
    maxdepth=3
)))

fig6.update_layout(
    grid= dict(columns=2, rows=1),
    margin = dict(t=0, l=0, r=0, b=0)
)


app = dash.Dash()

app.layout=html.Div([

    html.Img(
        className="logo", src=app.get_asset_url("image.png")
    ),

    html.Div([
        html.H1('FOOTBALL TRANSFERS'),
        html.H3('My subtitle')
    ], id='title_division', style={'border-style':'solid', 'border-color':'black'}),

    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id = 'year-slider',
            min=df_football['Year'].min(),
            max=df_football['Year'].max(),
            marks={str(i): '{}'.format(i) for i in df_football['Year'].unique()},
            value=2000
)
    ],style={'width': '200'}),

    # html.P(html.Div([
    #     dcc.Graph(id='line_plot', figure=fig2)
    # ])),
    html.P(html.Div([
        dcc.Graph(id='second_plot', figure=fig3)
    ])),

    html.P(html.Div([
        dcc.Graph(id='third_plot', figure=fig4)
    ])),
    html.P(html.Div([
        dcc.Graph(id='forth_plot', figure=fig5)
    ])),
    html.P(html.Div([
        dcc.Graph(id='fifth_plot', figure=fig6)
    ]))
], id='outer_division')


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = df_football.loc[df_football['Year'] == int(selected_year)]

    data = [go.Choropleth(
            locationmode='country names',
            locations= filtered_df.loc[filtered_df['Country_from'] == i]['Country_from'].unique(),
            z = [filtered_df.loc[filtered_df['Country_from'] == i]['Transfer_fee'].sum()],
            text = [filtered_df.loc[filtered_df['Country_from'] == i]['Name'].to_string()+'<br>'],
            colorscale = [
                [0.0, 'rgb(242,240,247)'],
                [0.2, 'rgb(218,218,235)'],
                [0.4, 'rgb(188,189,220)'],
                [0.6, 'rgb(158,154,200)'],
                [0.8, 'rgb(117,107,177)'],
                [1.0, 'rgb(84,39,143)']
            ],
            marker=go.choropleth.Marker(
                line=go.choropleth.marker.Line(
                    color='rgb(255,255,255)',
                    width=1
                )),
            colorbar=go.choropleth.ColorBar(
                title="Transfers")
            ) for i in filtered_df['Country_from'].unique()]

    return go.Figure(data=data, layout=layout_fig)
    # 
    # data_2 = TransfTeam.loc[TransfTeam["Year"] == str(selected_year)]
    # data_2 = data_2.sort_values(['Country'])
    # Country_names = data_2['Country'].unique()
    # Country_data = {Country: data_2.query("Country == '%s'" % Country)
    #                 for Country in Country_names}
    # 
    # data2 = [go.Scatter(
    #             type='scatter',
    #             x=Country['EarnedMoney'],
    #             y=Country['SpentMoney'],
    #             name=Country_names,
    #             text=Country['Team'],
    #             hovertemplate=
    #             '<b>%{text}</b>' +
    #             '<br><b>Spending</b>: €%{y}' +
    #             '<br><b>Earnings</b>: €%{x}' +
    #             '<br><b>Sales</b>: %{marker.size:}',
    #             mode='markers',
    #             marker=dict(size=Country['NumSignings'],
    #                         sizeref=0.5)
    # 
    # ) for Country_names, Country in Country_data.items()]

    # return go.Figure(data=data2, layout=layout_fig2)#, go.Figure(data=data, layout=layout_fig)

if __name__ == '__main__':
    app.run_server(debug=True)

