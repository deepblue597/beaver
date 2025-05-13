#######
# Objective: Using the iris dataset, develop a Distplot
# that compares the petal lengths of each class.
# File: '../data/iris.csv'
# Fields: 'sepal_length','sepal_width','petal_length','petal_width','class'
# Classes: 'Iris-setosa','Iris-versicolor','Iris-virginica'
######

# Perform imports here:
#%%
import plotly.figure_factory as ff 
import pandas as pd 
#%%

# create a DataFrame from the .csv file:
df = pd.read_csv('data/iris.csv')
#%%

# Define the traces

# HINT:
# This grabs the petal_length column for a particular flower
df[df['class']=='Iris-some-flower-class']['petal_length']

classes = ['Iris-setosa','Iris-versicolor','Iris-virginica']

# Define a data variable
data = [ df[df['class']==class_name]['petal_length'] for class_name in classes]
data


# Create a fig from data and layout, and plot the fig
# %%
fig = ff.create_distplot(data, classes)
fig.show() 
# %%
