
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas-docs.github.io/pandas-docs-travis/io.html#json
# + data source: http://jsonstudio.com/resources/
# ****

# In[3]:


import pandas as pd


# ## imports for Python, Pandas

# In[6]:


import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas-docs.github.io/pandas-docs-travis/io.html#normalization

# In[4]:


# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[7]:


# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[8]:


# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[9]:


# load json as string
json.load((open('data/world_bank_projects_less.json')))


# In[10]:


# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[3]:


# import modules
import pandas as pd
import json
from pandas.io.json import json_normalize
# loading data 
data = json.load(open('data/world_bank_projects.json'))
datanorm = json_normalize(data)
# Looking at the data
print(datanorm.head())
# Exercise 1:Finding the 10 countries with most projects
# Counting the number of entries for each country, and slice the first ten rows to get the top 10 countries with most projects.
top10_countries = datanorm.countryname.value_counts().head(10)
# Printing the answer of exercise 1
print('Exercise 1:The 10 countries with most projects are:')
list(top10_countries.index)


# In[4]:


# Exercise 2:Finding the top 10 major project themes (using column 'mjtheme_namecode')

datanorm2 = json_normalize(data, 'mjtheme_namecode',['id','countryname'])
top10 = datanorm2.code.value_counts().head(10)

#identifying project theme names for the top 10 projects
theme = pd.DataFrame(0, columns = ['name','code','times'], index = range(0,10))
for i in range(10):
    theme.code[i] = top10.index[i]
    names = datanorm2[datanorm2.code == top10.index[i]].name
    theme.name[i] = names.value_counts().index[0]
    theme.times[i] = top10[i]
print('Exercise 2:The top 10 major project themes are:')
print(theme['name'])


# In[5]:


#Exercise 3: Creating a dataframe with the missing names filled in.

#Dividing the original dataframe into two depending on names missing or not-x and y
x = datanorm2[datanorm2.name == '']
y = datanorm2[datanorm2.name != '']

for i in x.code.index:
    for j in y.code.index: 
        if x.code[i] == y.code[j]:
            x.name[i] = y.name[j]
            break
        else:
            continue
# combining missing x and y's and printing the dataframe
z= [x, y]
filled = pd.concat(z)
print(filled)

