#######
# Objective: Create a stacked bar chart from
# the file ../data/mocksurvey.csv. Note that questions appear in
# the index (and should be used for the x-axis), while responses
# appear as column labels.  Extra Credit: make a horizontal bar chart!
######

# Perform imports here:

#%%
import pandas as pd 
import plotly.graph_objects as go 
#%%

# create a DataFrame from the .csv file:
df = pd.read_csv('data/mocksurvey.csv' , index_col=0)
df
#%%

#%%
#what happens is 
# we take each column which are the responses 
# each response is added to the appropriate col 
# this happens via the x attribute 
# then we add a name which is each response 
# and we create a bar for each column in data 
data = [go.Bar(
    x = df.index, 
    y = df[response], 
    name = response 
    
) for response in df.columns]


# create a layout, remember to set the barmode here


layout = go.Layout(title = 'Survey' ,
                   barmode='stack')

fig = go.Figure(data = data , layout= layout)
fig.show() 
# create a fig from data & layout, and plot the fig.
# %%
