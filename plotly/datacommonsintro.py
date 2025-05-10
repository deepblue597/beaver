#%%
import datacommons_pandas as dc

# Import other required libraries
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

import json
# %%

# In the browser, we saw that the dcid for United States is country/USA
#greece = 'country/GRC'
greece = 'country/USA'

#%%
counties = dc.get_places_in([greece], 'County')[greece]
#%%
cities = dc.get_places_in([greece], 'City')[greece]
# %%
cities
# %%

# Get StatVarObservations for counties.
df_county = dc.build_multivariate_dataframe(counties, ['Count_Person', 'Median_Age_Person'])
# Get StatVarObservations for cities.
df_city = dc.build_multivariate_dataframe(cities, ['Count_Person', 'Median_Age_Person'])
# %%
df_city.head(5)
# %%
def add_name_col(df):
  # Add a new column called name, where each value is the name for the place dcid in the index.
  df['name'] = df.index.map(dc.get_property_values(df.index, 'name'))
  
  # Keep just the first name, instead of a list of all names.
  df['name'] = df['name'].str[0]
# %%
add_name_col(df_county)
df_county.head()
# %%
# Filter for all cities that have at least one person
df_city = df_city[df_city['Count_Person'] >= 1]
# %%
def plot_data(title, pd_table):
  """ Generate a scatter plot comparing median age and population count. """
  plt.figure(figsize=(12, 8))
  plt.title(title)
  plt.xlabel('Median Age in Years')
  plt.ylabel('Population Count (log scale)')
  
  # Scatter plot the information
  ax = plt.gca()
  ax.set_yscale('log')
  ax.scatter(pd_table['Median_Age_Person'], pd_table['Count_Person'], alpha=0.7)
# %%
# Generate the plot for county data
plot_data('Median Age vs. Population Count for region', df_county)
# %%
plot_data('Median Age vs. Population Count for Cities', df_city)
# %%
