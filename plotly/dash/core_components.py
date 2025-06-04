#%% 
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 
# %%
app = Dash() 

app.layout = html.Div(
    children=[ 
        html.Label('Dropdown'), 
        dcc.Dropdown(
            options = [ 
                'Heraklion', 
                'Thessaloniki', 
                'Athens'
            ], 
            value = 'Athens'
        ), 
        html.Label('Slider'), #String next to the component
        dcc.Slider(
            min = 0 , 
            max = 100 , 
            #step = 10, 
            #marks=None,
        ), 
        html.Label('Radio Items'), 
        dcc.RadioItems(
            options=[
                'New York City', 
                'Montreal',
                'San Francisco'],
            value =  'Montreal'
        )

    ]

)

#%%

if __name__ == '__main__': 
    app.run()
