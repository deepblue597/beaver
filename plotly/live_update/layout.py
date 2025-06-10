#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output , State
from dash import dcc, html 
import plotly.graph_objects as go
import json
import numpy as np 
from datetime import date

app = Dash() 

crash_free = 0 

    
app.layout = html.Div(
    children=[
        html.H1(
            id='text-update'
        ), 
        dcc.Interval(
            id = 'interval-comp', 
            interval=2000, 
            n_intervals= 0 
        )
    ]
)

@app.callback(
    Output(
        component_id='text-update', 
        component_property='children'
    ), 
    [
        Input(
            component_id='interval-comp', 
            component_property='n_intervals'
        )
    ]
)

def update_layout(n) :  
    return f'Page has been updated {n} times'


if __name__ == '__main__': 
    crash_free = 0 
    app.run() 