#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 
# %%
app = Dash() 

app.layout = html.Div(
    children= [ 
        dcc.Input(
            id='my-id', 
            value='Initial Text', 
            type='text',
            placeholder='input something' 

        ), 
        html.Div(
            id='my-div', 
            # style= dict(
            #     border = '2px solid'
            # )
        )
    ]
)

@app.callback(
        Output(
            component_id='my-div',
            component_property='children'
        ),
        [
            Input(
                component_id='my-id',
                component_property='value'
            
            )
        ]
)

def update_output_div(input_value) : 
    return f'You entered: {input_value}'



if __name__ == '__main__': 
    app.run() 