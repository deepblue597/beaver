#%% 
#######
# Objective: Using the file 2010YumaAZ.csv, develop a Line Chart
# that plots seven days worth of temperature data on one graph.
# You can use a for loop to assign each day to its own trace.
######

# Perform imports here:
import pandas as pd 
import plotly.graph_objects as go




# Create a pandas DataFrame from 2010YumaAZ.csv
df = pd.read_csv('data/2010YumaAZ.csv')
days = ['TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY','MONDAY']
#%% 
df2 = df.drop(columns='LST_DATE')
df2

#%% 
# df2.set_index('' , inplace= True)
# df2
# Reshape the DataFrame so that each day is a row and the time becomes the columns
#%%

#%% 
# Use a for loop (or list comprehension to create traces for the data list)
data = []
#data
#%%
for day in days:
    # What should go inside this Scatter call?
    trace = go.Scatter(
        x = df2['LST_TIME'], 
        y = df2[df2['DAY']== day]['T_HR_AVG'],
        mode = 'lines', 
        name = day 
    )
    data.append(trace)

# Define the layout

layout = go.Layout(title= 'line charts', hovermode='x') 



# Create a fig from data and layout, and plot the fig
fig = go.Figure(data=data , layout= layout)
fig.show()
# %%
