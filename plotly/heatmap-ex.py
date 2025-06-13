#######
# Objective: Using the "flights" dataset available
# from the data folder as flights.csv
# create a heatmap with the following parameters:
# x-axis="year"
# y-axis="month"
# z-axis(color)="passengers"
######
#%%
# Perform imports here:

import pandas as pd 
import plotly.graph_objects as go 

#%%
# Create a DataFrame from  "flights" data
df = pd.read_csv('data/flights.csv')
#%%
# Define a data variable
data = [ 
        go.Heatmap(
            x = df['year'], 
            y = df['month'], 
            z = df['passengers'], 
            colorscale='Portland'
        )]

layout = go.Layout(
    title='Airline Passengers'
)
fig = go.Figure(data = data , layout=layout) 
fig.show()



# Define the layout



# Create a fig from data and layout, and plot the fig
# %%
