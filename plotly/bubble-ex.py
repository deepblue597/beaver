#######
# Objective: Create a bubble chart that compares three other features
# from the mpg.csv dataset. Fields include: 'mpg', 'cylinders', 'displacement'
# 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'
######

#%% 
# Perform imports here:


import plotly.graph_objects as go 
import pandas as pd  

#%%
# create a DataFrame from the .csv file:

df = pd.read_csv('data/mpg.csv')    
# create data by choosing fields for x, y and marker size attributes


df.columns 
#%% 

df['acceleration'] = pd.to_numeric(df['acceleration'], errors='coerce')
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')

#%% 

data = [go.Scatter(          # start with a normal scatter plot
    x=df['acceleration'],
    y=df['horsepower'],
    text=df['name'],
    mode='markers',
    marker=dict(
        size=df['weight']/300,
        color = df['model_year'], 
        showscale = True
                ), # set the marker size
        

)]




#%%
# create a layout with a title and axis labels

layout = go.Layout(title= 'Vehicle acceleration vs horsepower', 
                   xaxis=dict(title = 'acceleration'), 
                   yaxis=dict(title = 'horsepower')
                   )







# create a fig from data & layout, and plot the fig
# %%
fig = go.Figure(data = data ,
                layout= layout)

fig.show() 
# %%
