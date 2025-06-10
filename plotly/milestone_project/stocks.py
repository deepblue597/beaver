#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output , State
from dash import dcc, html 
import plotly.graph_objects as go
import json
import numpy as np 
from datetime import date
import pandas_datareader.data as web
import finnhub
import os
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mattiuzc/stock-exchange-data")

print("Path to dataset files:", path)
#%%
# Setup client
df = pd.read_csv(path+'/indexData.csv')
df
# %%
app = Dash()

app.layout = html.Div(
    children=[
        html.H2(
            'Stock prices'
        ), 
        html.Div(
            children=[
                html.P('select stock symbols'), 
                dcc.Dropdown(
                    options= df['Index'].unique(), 
                    value = 'NYA', 
                    id='stock-dropdown',
                    multi=True
                    ),
            ], 
            style= dict(
                width = '40%', 
                display = 'inline-block', 
                verticalAlign='middle', 
                margin= '10px'
                
            )
        ), 
        html.Div(
            children= [
                html.P('Select start and end date') , 
                dcc.DatePickerRange(
                    id= 'date-picker-stock', 
                    month_format='Do MM, YY',
                    end_date_placeholder_text='Do MMM, YY',
                    start_date=date(2017, 6, 21)
)
            ], 
            style= dict(
                width = '20%', 
                display = 'inline-block', 
                verticalAlign='middle', 
                margin= '10px'
            )
        ), 
        html.Div(
            children=[
                html.Button(
                id='submit-btn',
                children='Submit', 
                n_clicks=0 
                )
            ], 
            style={
                'width':'20%', 
                'display' : 'inline-block' 
                }
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='stock-graph',
                     figure= go.Figure(
                         data=[
                             go.Scatter(
                                 x=[0,1],
                                 y=[0,1], 
                                 mode='lines'
                             )
                         ], 
                         layout = go.Layout(
                             title = 'stock prices',
                             xaxis={'title' : 'date'},  
                             yaxis={'title' : 'price'},
                         )
                     )
                )
            ]
        ), 

    ], 
    style= dict(
            margin = '10'
        )
)

@app.callback(
    Output(
        component_id='stock-graph', 
        component_property='figure'
    ),
    [
        Input(
        component_id='submit-btn', 
        component_property='n_clicks'
        )
    ], 
    [
        State(
            component_id='stock-dropdown', 
            component_property='value'
        ),
        State('date-picker-stock', 'start_date'), 
        State('date-picker-stock', 'end_date'), 

    ], 
    prevent_initial_call=True
)

def callback_stocks(clicks, stocks , start , end ):
    traces = [] 
    if isinstance(stocks, str):
        stocks = [stocks]
    for stock in stocks :  
        mask = (df['Index'] == stock)
        if start:
            mask &= (df['Date'] >= start)
        if end:
            mask &= (df['Date'] <= end)
        filtered = df[mask]
        traces.append(
            go.Scatter(
                x=filtered['Date'],
                y=filtered['Close'],  # or the correct price column
                mode='lines',
                name=stock
            )
        )
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title=f'Stock prices for {stocks}',
            xaxis={'title': 'date'},
            yaxis={'title': 'price'},
        )
    )
    return fig

if __name__ == '__main__' : 
    
    app.run()