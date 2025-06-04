#%% 
from dash import Dash
from dash import dcc, html 
import plotly.graph_objects as go 
#%%

app = Dash()
'''
When you have multiple components inside a div 
you need a list o/w dont need a list 
just to be sure though make it a list
'''
app.layout = html.Div(
    #first thing that is added is children but its better to specify 
    children=[ 
        'Hello mum', 
        html.Div(
            children = [
                'This is an inner Div'
                ], 
            style= dict(
                color = 'red' , 
                border = '2px purple solid'
            ) 

        ), 
        html.Div(
            children= [ 
                'another inner div' 
            ],

            style= dict(
                color = 'pink', 
                border = '2px solid black'
            ) 
            
        )
    ], 
    style= dict(
        color = 'green', 
        border = '2px blue solid', 

    )
) 



#%%

if __name__ == '__main__': 
    app.run() 