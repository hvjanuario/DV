import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dataset Processing

df_football = pd.read_csv('DATABASE.csv')

df_football_0 = df_football.loc[df_football['Year'] == 2000]

data= [go.Choropleth(dict(
    locationmode='country names',
    locations =  df_football_0.loc[df_football_0['Country_from'] == i]['Country_from'].unique(),
    z = [df_football_0.loc[df_football_0['Country_from'] == i]['Transfer_fee'].sum()],
    text = df_football_0.loc[df_football_0['Country_from'] == i]['Name'].to_string(),
    colorscale = 'Blues',
    autocolorscale=True,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '€',
    colorbar_title='Football',
    colorbar_tickmode = 'auto'
)) for i in df_football_0['Country_from'].unique()]

layout_fig = dict(geo=dict(
    showframe=False,
    showcoastlines=False,
    projection_type='equirectangular'
    ),
    height=600,
    title=dict(text='Football'),
    annotations = [dict(
        x=0.55,
        y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
            showarrow = False
            )],
)

fig_choropleth = go.Figure(data=data, layout=layout_fig)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_football['Year'].min(),
        max=df_football['Year'].max(),
        value=df_football['Year'].min(),
        marks={str(Year): str(Year) for Year in df_football['Year'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = df_football.loc[df_football['Year'] == int(selected_year)]

    fig_f = [go.Choropleth(
        locationmode='country names',
        locations= filtered_df.loc[filtered_df['Country_from'] == i]['Country_from'].unique(),
        z = [filtered_df.loc[filtered_df['Country_from'] == i]['Transfer_fee'].sum()],
        text = [filtered_df.loc[filtered_df['Country_from'] == i]['Name'].to_string()],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix='€',
        colorbar_title='Football',
        colorbar_tickmode='auto'
) for i in filtered_df['Country_from'].unique()]

    return go.Figure(data=fig_f, layout=layout_fig)


if __name__ == '__main__':
    app.run_server(debug=True)
