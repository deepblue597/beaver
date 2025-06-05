#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go
import base64
import os

# %%

app = Dash()  

#to display jpeg 
def encode_image(image_file): 
    with open(image_file, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
    return f'data:image/png;base64,{encoded}'
# %%

df = pd.read_csv('../data/wheels.csv')
df 
# %%
app.layout = html.Div(
    children= [ 
        dcc.RadioItems(
            id= 'wheels', 
            options=[ 
                i for i in df['wheels'].unique() 
            ], 
            value = 1 

        ), 
        html.Div(
            id='wheels-output'

        ), 
        html.Hr(), 
        dcc.RadioItems(
            id = 'colors',
            options = [ color for color in df['color'].unique()], 
            value = df['color'][0] 
        ), 
        html.Div(
            id = 'colors-output'
        ),
        html.Img(
            id = 'display-image', 
            src = 'children', #
            height=300 
        ) 

    ], 
            style= dict( 
            fontFamily  = 'helvetica', 
            fontSize = 15 
        )
)
# %%
@app.callback(
        Output(
           component_id='wheels-output', 
           component_property='children' 
        ), 
        [
            Input(
                component_id='wheels', 
                component_property='value'
            )
        ]
)
def callback_wheels(wheels) : 
    return f'you chose {wheels} wheel(s)'
# %%
@app.callback(
        Output(
            component_id='colors-output', 
            component_property='children'
        ), 
        [
            Input(
                component_id='colors', 
                component_property='value'
            )
         ]
)
def callback_color(color): 
    return f'You chose {color} color'

@app.callback(
        Output(
            component_id='display-image', 
            component_property='src'
        ),
        [
            Input(
                component_id='wheels', 
                component_property='value'
            ), 
            Input(
                component_id='colors', 
                component_property='value'
            )
        ]
)
def callback_image(wheel , color) : 
    path ='../data/images'
    image_filename = df[(df['wheels'] == wheel) & (df['color'] == color)]['image'].values[0]
    full_path = os.path.join(path, image_filename)
    return encode_image(full_path)# %%

if __name__ == '__main__': 
    app.run() 
# %%
