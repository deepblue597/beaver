#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output , State
from dash import dcc, html 
import plotly.graph_objects as go 
# %%

app = Dash() 

app.layout = html.Div(
    children= [ 
        dcc.Input(
            id='number-in',
            type='number', 
            value = 1 

        ), 
        html.H1(
            id='number-out'
        ), 
        html.Button(
            id='submit-btn', 
            n_clicks=0, 
            children='Submit'
        )
    ]
)

@app.callback(
    Output(
        component_id= 'number-out',
        component_property= 'children'
    ), 
    [
        Input(
        component_id='submit-btn', 
        component_property='n_clicks'
        )
    ], 
    [
        State(
            component_id='number-in',
            component_property='value' 

        )
    ], 
    prevent_initial_call=True

)

def output(n_clicks , number) : 
    return f'number submitted:{number}. Number of times clicked: {n_clicks}'

if __name__ == '__main__': 
    app.run() 

