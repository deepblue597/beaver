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