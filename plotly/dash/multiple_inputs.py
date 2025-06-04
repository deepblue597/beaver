#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 
# %%

df = pd.read_csv('../data/mpg.csv')
#%%
df
#%%
app = Dash() 

#%%

features = df.columns # the cols of data  


app.layout = html.Div(
    children=[ 
        html.Div(
            [
                dcc.Dropdown(
                    id='xaxis',
                    options = [dict(
                        label = i , 
                        value = i 
                    ) for i in features],  
                    value=features[0]
        )], 
            style= dict(
                width='48%', 
                display = 'inline-block'
            )
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='yaxis',
                    options= features,
                    #[dict(
                    #     label = i , value = i 
                    # ) for i in features], #its better to use dict with name and value but oh well 
                    value = features[1]
                )
            ], 
            style= dict(
                width='48%', 
                display = 'inline-block'
            )
        ), 
        dcc.Graph(
            id='features-graph'
        )

    ]
)

@app.callback(
    Output(component_id='features-graph', component_property='figure'),
    [
        Input(component_id='xaxis', component_property='value'), 
        Input(component_id='yaxis' , component_property='value')
    ]
)

def update_graph(xaxis , yaxis) : 
    
    plot = go.Scatter(
        x = df[xaxis], 
        y=df[yaxis], 
        mode='markers',
        opacity=0.7, 
        #name = df['name']
        text=df['name'],
        hoverinfo='text+x+y'
    )
    return dict(
        data = [plot] ,
        layout = go.Layout(
            title='Cars', 
            xaxis= dict(
                title = xaxis
            ), 
            yaxis= dict(
                title = yaxis
            )
        ) 
    ) 

#%% 

if __name__ == '__main__' : 
    app.run() 