'''
Distribution plots or dist plots for short.

Typically layer three plots on top of one another.

The first plot is a histogram where each data point is placed inside a bin of similar values.

The second is a rug plot.

This is where marks are placed along the x axis for every single data point, which lets you see the

actual distribution of values inside each bin.

Then the third plot, the distribution plot shows, is going to include a kernel density estimate,

plot or KDE for short.
'''

#%% 
import plotly.figure_factory as ff 
import pandas as pd 
import numpy as np 
# %%


x1 = np.random.randn(1000) + 3  
x2 = np.random.randn(1000) 
x3 = np.random.randn(1000) - 3 
x4 = np.random.randn(1000) - 6 

hist_data = [x1, x2 , x3 , x4] 
# %%
group_labels = ['x1','x2','x3','x4' ]
# %%
fig = ff.create_distplot(hist_data= hist_data , group_labels= group_labels, bin_size=[0.2 , 0.1 , 0.3 , 0.1])
fig.show() 
# %%

snodgrass = [.209,.205,.196,.210,.202,.207,.224,.223,.220,.201]
twain = [.225,.262,.217,.240,.230,.229,.235,.217]

hist_data = [snodgrass,twain]
group_labels = ['Snodgrass','Twain']

fig = ff.create_distplot(hist_data, group_labels, bin_size=[.005,.005])
fig.show() 
# %%
