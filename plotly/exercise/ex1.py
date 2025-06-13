#%%
#######
# Objective: build a dashboard that imports OldFaithful.csv
# from the data directory, and displays a scatterplot.
# The field names are:
# 'D' = date of recordings in month (in August),
# 'X' = duration of the current eruption in minutes (to nearest 0.1 minute),
# 'Y' = waiting time until the next eruption in minutes (to nearest minute).
######

# Perform imports here:

import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 
#%%


# Launch the application:
app = Dash() 

# Create a DataFrame from the .csv file:

df = pd.read_csv('../data/OldFaithful.csv')

#%% 
df 
#%% 
scatter = go.Scatter(
    x = df['X'], 
    y = df['Y'], 
    mode= 'markers'
)

layout = go.Layout(
    title='Old Faithful', 
    xaxis= dict(
        title = 'Duration of eruption (minutes)'
    ), 
    yaxis= dict(
        title = 'Interval between eruptions'
    )
)
# %%
#%%

# Create a Dash layout that contains a Graph component:

app.layout = html.Div(

    children= [ 
        dcc.Graph ( 
            id = 'oldFaithful', 
            figure= dict ( 
                data = [ scatter], 
                layout = layout  
            )
        )
    ]

)

#%% 

if __name__ == '__main__': 
    app.run() 
















# Add the server clause:
# %%
