#%%
import numpy as np 


# %%
a = np.arange(1, 10)
# %%
a
# %%
type(a)
#%% 
rand = np.random.randint(0 , 100, (3, 4))
rand

#%% 

lin = np.linspace(0, 10, 6)
lin 

#%% 

#generate radom numbs over and over again 
# we need a random seed to generate the same random numbers

same_rand = np.random.seed(41) 
np.random.randint(0, 100, 10)

#%% 
#max , min etc 

arr = np.random.randint(0, 100, 10 )
arr.max()
arr.min()
arr.mean()
arr.argmax() # index loc of max 
arr.reshape(2, 5) # reshape the array

#%% 

matrix = np.arange(0, 100).reshape(10, 10)
matrix 
#%% 

matrix[: , 2]
matrix[2 , :] 
#%% masking 

mask = matrix > 50
mask # brings boolean values where true > 50 false < 50 

#%% 
matrix[matrix>50]

#%% pandas crash course 
import pandas as pd

#%% 

df = pd.read_csv('salaries.csv')
df
#%% 

#select columns 
df['Salary']
#%% select mulutple columns 
df[['Salary', 'Name']]

#%% min max mean for columns 

df['Salary'].max()
df['Salary'].min()
df['Salary'].mean()

#%% filtering 

df[df['Salary'] > 100000]
df['Age'] > 30
df[df['Age'] > 30]

#%% some features of pandas 

df['Age'].unique() # unique values in the column
df.describe() # gives the summary of the data
df.info() # gives the info of the data

#%% generate pandas data frame

mat = np.arange(0 , 10).reshape(5, 2)
df = pd.DataFrame(mat , columns=['A', 'B'])
df 