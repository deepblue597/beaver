#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go
import json
import numpy as np 
# %%
app = Dash()

df = pd.read_csv('../data/mpg.csv')
# adding noise/jitter 
df['year'] = np.random.randint(-4 , 5 , len(df)) * 0.1 + df['model_year']

app.layout = html.Div([
    html.Div([   # this Div contains our scatter plot
    dcc.Graph(
        id='mpg_scatter',
        figure={
            'data': [go.Scatter(
                x = df['year']+1900,  # our "jittered" data
                y = df['mpg'],
                text = df['name'],
                hoverinfo = 'text',
                mode = 'markers'
            )],
            'layout': go.Layout(
                title = 'mpg.csv dataset',
                xaxis = {'title': 'model year'},
                yaxis = {'title': 'miles per gallon'},
                hovermode='closest'
            )
        }
    )], style={'width':'50%','display':'inline-block'}),
    html.Div([  # this Div contains our output graph
    dcc.Graph(
        id='mpg_line',
        figure={
            'data': [go.Scatter(
                x = [0,1],
                y = [0,1],
                mode = 'lines'
            )],
            'layout': go.Layout(
                title = 'acceleration',
                margin = {'l':0}
            )
        }
    )
    ], style={'width':'20%', 'height':'50%','display':'inline-block'})
])

@app.callback(
    Output('mpg_line', 'figure'),
    [Input('mpg_scatter', 'hoverData')])
def callback_graph(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    fig = {
        'data': [go.Scatter(
            x = [0,1],
            y = [0,60/df.iloc[v_index]['acceleration']],
            mode='lines',
            line={'width':2*df.iloc[v_index]['cylinders']}
        )],
        'layout': go.Layout(
            title = df.iloc[v_index]['name'],
            xaxis = {'visible':False},
            yaxis = {'visible':False, 'range':[0,60/df['acceleration'].min()]},
            margin = {'l':0},
            height = 300
        )
    }
    return fig


if __name__ == '__main__' : 
    
    app.run()