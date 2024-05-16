from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

df = pd.read_csv('WayPoint_coords.csv')
df_ways = pd.read_csv('Optimal_routes.csv')

app = Dash()

app.layout = html.Div([
    html.H1(children='Маршруты Иркутской области', style={'textAlign':'center'}),
    html.Div(
        dcc.Dropdown(df['city'].unique(),
                      'Иркутск',
                        id='dropdown-selection',
                          style={'width': '100%'}) # выбор города
                          ),
    html.Div(
        [dcc.Graph(id='map',style={'width': '100%','height': 600})
        ])
])

@callback(
    Output('map', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value:list):
    dff = df[df.city==value]
    dff_ways = df_ways[df_ways.city==value]

    fig1 = px.scatter_mapbox(dff, 
                            lat='lat', lon='lon',
                            color_discrete_sequence=['gray'],
                            hover_name='short_name',
                            hover_data=['Наименование маршрута','address','source','N_point'])
    
    fig2 = px.line_mapbox(dff_ways,
                          lat='lat', lon='lon',
                          color='Наименование маршрута').add_traces(fig1.data)
    
    
    fig2.update_layout(title_text='Маршруты',
                      mapbox_style="open-street-map",
                      mapbox_center={
                          'lat':(dff['lat'].max()+dff['lat'].min())/2,
                          'lon':(dff['lon'].max()+dff['lon'].min())/2
                          })
    return fig2


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
