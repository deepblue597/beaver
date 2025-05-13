#%% 
import plotly.graph_objects as go 
import numpy as np
import pandas as pd  
# %%
df = pd.read_csv('data/abalone.csv') 
#np.random.choice()
# %%
data1 = np.random.choice(df['rings'] , 40 , replace=False)

data2 = np.random.choice(df['rings'] , 20 , replace=False )
#%%

data = [
    go.Box(y = data1, 
           name = 'data1'), 
    go.Box(y = data2, 
           name = 'data2') 
]
# %%
fig = go.Figure(data = data ) 
fig.show() 
# %%
