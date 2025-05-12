#%% 
import plotly.graph_objects as go 
import pandas as pd 
import plotly.offline as pyo 
# %%
df = pd.read_csv('data/2018WinterOlympics.csv')
# %%
df

# %%
data = [ go.Bar(
    x = df['NOC'], 
    y = df['Total']

)]

layout = go.Layout(title='Medals')

fig = go.Figure(data = data , layout= layout)

fig.show() 
# %%

trace1 = go.Bar(
    x = df['NOC'],
    y = df['Gold'],
    name = 'Gold', 
    marker= dict(color = '#FFD700')
)

trace2 = go.Bar(
    x = df['NOC'],
    y = df['Silver'],
    name = 'Silver', 
    marker= dict(color = '#9EA0A1')
)

trace3 = go.Bar(
    x = df['NOC'],
    y = df['Bronze'],
    name = 'Bronze', 
    marker= dict(color = '#CD7F32')
)


data = [ trace1 , trace2 , trace3]
# %%

#Nested bar chart 

fig = go.Figure(data = data , layout= layout)

fig.show()
# %% staked bar plot 
layout = go.Layout(title='Medals' , barmode='stack')

fig = go.Figure(data = data , layout= layout)

fig.show() 


# %%
