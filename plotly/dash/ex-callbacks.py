#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 

#%%
app = Dash() 

app.layout = html.Div(
    children= [ 
        dcc.RangeSlider(
            id='slider',
            min = -5, 
            max = 6,
            step=1  
        ),
        html.Div(
            id='multiplication'

        )
    ]
)

@app.callback(
    Output(
        component_id='multiplication', 
        component_property='children'
    ), 
    [
        Input(
            component_id='slider', 
            component_property='value'
        )
    ]
)
def callback_multiplication(slider_range) : 
    low , up = slider_range
    return low * up 

if __name__ == '__main__': 
    app.run() 