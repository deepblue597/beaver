#%% 
import plotly.graph_objects as go 
import pandas as pd 
# %%
df = pd.read_csv('data/mpg.csv')
# %%
#xbins shows the data between these valus only 
data = [go.Histogram(
    x = df['mpg'], 
    xbins=dict(
        start =0  , 
        end =50, 
        size = 5  
        )
    )
]

layout = go.Layout(title='histogram', 
                   yaxis=dict(title = 'mpg'))

fig = go.Figure(data= data , layout= layout)
fig.show() 
# %%
df = pd.read_csv('data/abalone.csv')
data = [ go.Histogram(
     
    x = df['length'], 
    xbins= dict(
        start = 0 , 
        end = 1 , 
        size = 0.02 
    )
)]

# %%

layout = go.Layout(title='Histogram', 
                   yaxis=dict(title = 'length'))

fig = go.Figure(data= data , layout= layout)
fig.show() 
# %%
