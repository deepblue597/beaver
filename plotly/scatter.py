#%% 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go

# Example data
y_true = [3, 5, 2, 8, 7]
y_predicted = [2.8, 5.1, 2.2, 7.8, 6.9]

# Create a DataFrame
df = pd.DataFrame({'y_true': y_true, 'y_predicted': y_predicted})
df
#%%
# Create a scatter plot with two traces
fig = go.Figure()

# Add predicted values as the main scatter plot
fig.add_trace(go.Scatter(
    x=df['y_true'], 
    y=df['y_predicted'], 
    mode='markers', 
    name='Predicted Values',
    marker=dict(color='blue', size=10)
))

# Add y_true values as separate dots
# fig.add_trace(go.Scatter(
#     x=df['y_true'], 
#     y=df['y_true'], 
#     mode='markers', 
#     name='True Values',
#     marker=dict(color='red', size=8, symbol='circle')
# ))

# Add a diagonal reference line (y = x)
fig.add_trace(go.Scatter(
    x=[min(y_true), max(y_true)], 
    y=[min(y_true), max(y_true)], 
    mode='lines', 
    name='Reference Line',
    line=dict(color='red', dash='dash')
))

# Update layout
fig.update_layout(
    title='True vs Predicted Values',
    xaxis_title='True Values',
    yaxis_title='Predicted Values',
    showlegend=True
)

# Show the plot
fig.show()
#%% 

# import plotly.express as px
# df = px.data.iris() # iris is a pandas DataFrame
# df

np.random.seed(42) 

# %%
random_x = np.random.randint(1 , 101 , 100 ) 
random_y = np.random.randint(1 , 101 , 100 )

#%% 

#For our case in live data we need to use go.Scatter since px.scatter is not working 
#No, you cannot directly use plotly.express.scatter (px.scatter) in place of plotly.graph_objects.Scatter (go.Scatter) when working with plotly.subplots.make_subplots. This is because px.scatter returns a complete Figure object, while go.Scatter creates a trace that can be added to a subplot.

# Why?
# px.scatter: Generates a standalone Figure object, which includes data, layout, and other configurations.
# go.Scatter: Creates a single trace (data series) that can be added to a Figure or subplot.


# marker points instead of lines 
data = go.Scatter(
    x = random_x , 
    y= random_y , 
    mode = 'markers', 
    marker=dict(
        size = 8, 
        color = 'rgb(51 , 125 , 208 )',
        symbol = '5', 
        line = dict(
            width = 2 
        )
    ) 
)

#add labels , hover mode etc 
# this cannot be used with live updates because it does not update the layout and causes errors with the values 
layout = go.Layout(title= 'Random points' , xaxis=dict(title = 'xaxis') , 
                   yaxis=dict(title = 'y axis'), hovermode='closest')

fig = go.Figure(data = data , layout=layout ) 

fig.show() 