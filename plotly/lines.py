#%% 
import plotly.graph_objects as go
import numpy as np

#%% 

np.random.seed(56) 
#%%

x_values = np.linspace(0 , 1 , 100 ) 
y_values = np.random.randn(100 ) 

#%% 

trace0 = go.Scatter(x = x_values , y = y_values+5, mode = 'markers' , name = 'markers')

trace1 = go.Scatter(x = x_values , y= y_values , mode = 'markers+lines' , name='markers+lines' )

trace2 = go.Scatter(x = x_values , y = y_values-5 , name = 'lines')

#hovermode x means that it will show all the y values when you hover over an x value
layout = go.Layout(title= 'line charts', hovermode='x') 
# we use the data to add multiple data inside 
data = [trace0 , trace1 , trace2]
fig = go.Figure(data = data , layout=  layout)
fig.show() 
#%% same thing as above but with add trace 
fig = go.Figure( layout=  layout)
fig.add_trace(trace = trace0 ) 
fig.add_trace(trace= trace1)
fig.show() 

#%% 