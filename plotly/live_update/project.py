#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output , State
from dash import dcc, html 
import plotly.graph_objects as go
import json
import numpy as np 
from datetime import date
import requests
import flightradar24

app = Dash() 

counter_list = [] 

app.layout = html.Div(
    children=[
        
        html.Div(
            children=[
                html.Iframe(
                    src='https://dash.plotly.com/dash-core-components/dropdown', 
                    height = 500,
                    width = 1200 
                )
            ]
        ), 
        html.Div(
            children=[
                html.Pre(
                    id = 'counter-text', 
                    children= 'Active Flights', 
                    
                ),
                dcc.Graph(
                    
                    id= 'live-update-graph',
                    style=dict(
                        width = 1200
                    )
                    
                    ), 
                dcc.Interval(
                    id='interval-comp', 
                    interval=6000, 
                    n_intervals=0
                )
            ]
        )
    ]
)

@app.callback(
    Output(
        component_id='counter-text', 
        component_property='children'
    ), 
    [
        Input(
            component_id='interval-comp', 
            component_property='n_intervals'
        )
    ]
)
def update_layout(n): 
    try:
        response = requests.get("https://opensky-network.org/api/states/all")
        #data = response.json()
        #if response.status_code != 200:
        active_flights = np.random.randint(10000 , 15000)
        #else: 
        #    active_flights = len(data['states'])
        
        counter_list.append(active_flights)
        return f"Active Flights: {active_flights}"
    except Exception as e:
        return f"Error fetching data: {e}"    


@app.callback(
    Output(
        component_id='live-update-graph', 
        component_property='figure'
    ), 
    [
        Input(
            component_id='interval-comp', 
            component_property='n_intervals'
        )
    ]
)
def update_graph(n): 
        
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(len(counter_list))), 
                    y=counter_list, 
                    mode='lines+markers'
                    
                )
            ]
        )
        
        return fig

       




if __name__ == '__main__': 
    app.run() 