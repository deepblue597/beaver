#%%
import plotly.graph_objects as go 
import pandas as pd  
# %%
df = pd.read_csv('data/mpg.csv')
df
# %%
df.columns
# %%
# it had an issue because it saw it as string 
# so it wasnt ordered 
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')

data = [go.Scatter(          # start with a normal scatter plot
    x=df['horsepower'],
    y=df['mpg'],
    text=df['name'],
    mode='markers',
    marker=dict(
        size=df['weight']/300,
        color = df['cylinders'], 
        showscale = True
                ), # set the marker size
        

)]

layout = go.Layout(
    title='Vehicle mpg vs. horsepower',
    xaxis = dict(title = 'horsepower'), # x-axis label
    yaxis = dict(title = 'mpg'),        # y-axis label
    
)
fig = go.Figure(data=data, layout=layout)
fig.show() 
# %%
 
# %%
