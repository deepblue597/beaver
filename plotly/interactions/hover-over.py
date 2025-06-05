
#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go
import json
# %%

app = Dash() 

df = pd.read_csv('../data/wheels.csv') 

app.layout = html.Div([
    html.Div([
    dcc.Graph(
        id='wheels-plot',
        figure={
            'data': [
                go.Scatter(
                    x = df['color'],
                    y = df['wheels'],
                    dy = 1,
                    mode = 'markers',
                    marker = {
                        'size': 12,
                        'color': 'rgb(51,204,153)',
                        'line': {'width': 2}
                        }
                )
            ],
            'layout': go.Layout(
                title = 'Wheels & Colors Scatterplot',
                xaxis = {'title': 'Color'},
                yaxis = {'title': '# of Wheels','nticks':3},
                hovermode='closest'
            )
        }
    )], style={'width':'30%', 'float':'left'}),

    html.Div([
    html.Pre(id='hover-data', style={'paddingTop':35})
    ], style={'width':'30%'})
])


@app.callback(
        Output(
            component_id='hover-data', 
            component_property='children'
        ), 
        [ 
            Input(
                component_id='wheels-plot', 
                component_property='hoverData'
            )
        ]
)
def callback_image( hoverData) : 
    return json.dumps(
        hoverData, 
        indent=2
    )

if __name__ == '__main__': 
    app.run() 