#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate TMDb movie dataset
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# **This analysis treat with TMDb movie dataset to answer about some questions based on adjusted currancy value that corrected for inflation or gross domestic product (GDP) to cover for period of movies release years that about 55 year from 1960 till 2015.**
# 
# ### Questions is:
# 
# * **What's period that movies released duration?**
# * **Which most popular movie weighted by voters and rating number?**
# * **Movie with highest or lowest adjusted budget?**
# * **Which movie made the highest and lowest adjusted revenue?**
# * **Which movie Has the highest or lowest adjusted profit?**
# * **Which movie has longest and shorest runtime?**
# * **What's avearage runtime of movies?**
# * **Which year has the highest count release of movies?**
# * **Which year has the highest adjusted profit?**
# * **Which genre has the most count of released movies?**
# * **Which most star acted in movies?**
# * **Which is production company with highest number of released movies?**
# * **Which is director who directed maximum Movies?**

# In[2]:


# Import statements for all of the packages that you plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties

# In[3]:


# Load data and print out a few lines.
df=pd.read_csv('tmdb-movies.csv')
df.head()


# In[4]:


# Display Data Frame information
df.info()


# In[4]:


#Display total count of null values in each column
df.isnull().sum()


# In[5]:


#Check duplicated values
df.duplicated().sum()


# ### Data Cleaning :
# * Remove duplicate data
# * Convert columns data to suitable type and remove that not useful in our processing
# * Remove null and zeros rows

# In[6]:


# Remove duplicated Values and check after
df.drop_duplicates(inplace=True)
df.duplicated().sum()


# In[7]:


#Convert 'release_date' column to datatime format and insure from some columns tepe then check after
df['release_date']=pd.to_datetime(df['release_date'])
df[['cast','genres','production_companies']] = df[['cast','genres','production_companies']].astype(str)
df[['budget_adj','revenue_adj']]=df[['budget_adj','revenue_adj']].applymap(np.int64)

df.dtypes


# In[8]:


#Romve columns that not be useful in analysis
df.drop([ 'id', 'imdb_id', 'homepage', 'tagline','keywords', 'overview'],axis=1,inplace=True)


# In[9]:


# Remove all null data in 'budget_adj','revenue_adj' columns and check null values after
df[['budget_adj','revenue_adj']]=df[['budget_adj','revenue_adj']].replace(0, np.NAN)
df.dropna(subset=['budget_adj','revenue_adj'],inplace=True)

# Display data frame shape after removing
df.shape


# In[10]:


#Creating more columns for analysing
df['vote_popularity']=df['vote_count']*df['vote_average']*df['popularity']
df['Profit_adj']=df['revenue_adj']-df['budget_adj']


# In[11]:


df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# ### Research Question 1 : What's period that movies released duration?

# In[11]:


#Display period of movies database
period=df['release_year'].max()-df['release_year'].min()
'Movies database cover period about {} years from {} to {}'.format(period,df['release_year'].min(),df['release_year'].max())


# ### Research Question 2 : Which most popular movie weighted by voters and rating number?

# In[12]:


#Display most max. and min. vote popularity and popularity in movies
df[df['vote_popularity'] == df['vote_popularity'].max()]


# **Most popular movie weighted by voters and rating number is "Interstellar" in 2014**

# ### Research Question 3 : Which movie with highest or lowest adjusted budget?

# In[13]:


#Display most max. and min. adjusted budget in movies
higher_budget_adj=df[df['budget_adj'] == df['budget_adj'].max()]
lower_budget_adj=df[df['budget_adj'] == df['budget_adj'].min()]
pd.concat([higher_budget_adj, lower_budget_adj], axis=0)


# **Movie with highest adjusted budget is "The Warrior's Way" in 2010 and lowest one is "Love, Wedding, Marriage" in 2011**

# ### Research Question 4 : Which movie made the highest and lowest adjusted revenue ?

# In[14]:


#Display most max. and min. adjusted revenue in movies
higher_revenue_adj=df[df['revenue_adj'] == df['revenue_adj'].max()]
lower_revenue_adj=df[df['revenue_adj'] == df['revenue_adj'].min()]
pd.concat([higher_revenue_adj, lower_revenue_adj], axis=0)


# **Movie with highest adjusted revenue is "Avatar" in 2009 and lowest one is "Shattered Glass
# " in 2003**

# ### Research Question 5 : Which movie Has the highest or lowest adjusted profit?

# In[15]:


#Display most max. and min. adjusted Profit in movies
higher_profit_adj=df[df['Profit_adj'] == df['Profit_adj'].max()]
lower_profit_adj=df[df['Profit_adj'] == df['Profit_adj'].min()]
pd.concat([higher_profit_adj, lower_profit_adj], axis=0)


# **Movie with highest adjusted profit is "Star Wars" in 1977 and lowest one is "The Warrior's Way" in 2010**

# ### Research Question 6 : Which movie has longest and shorest runtime?

# In[16]:


#Display most max. and min. runtime of movies
longest_runtime=df[df['runtime'] == df['runtime'].max()]
shortest_runtime=df[df['runtime'] == df['runtime'].min()]
pd.concat([longest_runtime, shortest_runtime], axis=0)


# **Movie with longest runtime is "Carlos" in 2010 and lowest one is "Kid's Story" in 2003**

# ### Research Question 7 : What's avearage runtime of movies?

# In[18]:


#Display runtime of movies statistics
df['runtime'].describe()


# In[42]:



df['runtime'].plot(kind='hist',figsize=(12,6),fontsize=11)
plt.xlabel('Genres',fontsize=11)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Most genres release of movies',fontsize=16)
plt.show()


# **Avearage runtime of movies is nearly 109 minutes**

# ### Research Question 8 : Which year has the highest count release of movies?

# In[19]:


#Display Most count of movies yearly
movies_count=df['release_year'].value_counts()
movies_count


# In[102]:


#Make chart as visual display for most count of movies yearly
movies_count.plot(kind='bar',figsize=(17,6),fontsize=11)
plt.xlabel('year',fontsize=11)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Movies Yearly',fontsize=16)
plt.show()


# **The year has the highest count release of movies is 2011 with 198 movies in it**

# ### Research Question 9 : Which year has the highest adjusted profit?

# In[20]:


#Display Most Adjusted profit of movies yearly
most_profit_year = df.groupby('release_year')['Profit_adj'].sum()
most_profit_year.sort_values(ascending=False)


# In[21]:


#Make chart as visual display for most adjusted profit movies yearly
most_profit_year.plot(kind='line',figsize=(17,6),fontsize=11)
plt.xlabel('Release Year',fontsize=14)
plt.xticks(rotation=70)
plt.ylabel('Adjusted Profit',fontsize=11)
plt.title('Adjusted Profit Yearly',fontsize=16)
plt.show()


# **The year has the highest adjusted profit is 2015 with nearly 17.5 billion Dollar**

# ### Research Question 10 : Which genre has the most count of released movies?

# In[22]:


#Display most genres release of movies
genres_count=pd.Series(df['genres'].str.cat(sep = '|').split('|')).value_counts()
genres_count


# In[112]:


#Make chart as visual display for most genres count of movies
genres_count.plot(kind='bar',figsize=(17,6),fontsize=11)
plt.xlabel('Genres',fontsize=11)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Most genres release of movies',fontsize=16)
plt.show()


# **The genre has the most count of released movies is "Drama" with 1755 movies**

# ### Research Question 11 : Which most star acted in movies?

# In[23]:


#Display Most 20 actors played in movies
cast_count=pd.Series(df['cast'].str.cat(sep = '|').split('|')).value_counts().iloc[:20]
cast_count


# In[113]:


#Make chart as visual display for most 20 actor play in movies
cast_count.plot(kind='bar',figsize=(17,6),fontsize=11)
plt.xlabel('Actor',fontsize=11)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Most 20 actor play in movies',fontsize=16)
plt.show()


# **Which most star acted in movies is "Robert De Niro" with 52 movies**

# ### Research Question 12 : Which is production company with highest number of released movies?

# In[24]:


#Display Most 20 production companies
most_production_companies=pd.Series(df['production_companies'].str.cat(sep = '|').split('|')).value_counts().iloc[:20]
most_production_companies


# In[116]:


#Make chart as visual display for most 20 production companies
most_production_companies.plot(kind='bar',figsize=(17,6),fontsize=11)
plt.xlabel('Production Companies',fontsize=10)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Most 20 production companies',fontsize=16)
plt.show()


# **The production company with highest number of released movies is "Universal Pictures" with 329 movies**

# ### Research Question 13 : Which is director who directed maximum Movies?

# In[25]:


#Display Most 20 director directed movies
most_director=pd.Series(df['director'].str.cat(sep = '|').split('|')).value_counts().iloc[:20]
most_director


# In[119]:


#Make chart as visual display for most 20 director directed movies
most_director.plot(kind='bar',figsize=(17,6),fontsize=11)
plt.xlabel('Director',fontsize=11)
plt.xticks(rotation=70)
plt.ylabel('Movies count',fontsize=14)
plt.title('Most 20 director directed movies',fontsize=16)
plt.show()


# **The director who directed maximum Movies is "Steven Spielberg" with 28 movies**

# <a id='conclusions'></a>
# ## Conclusions
# 
# **After analysis for TMDb database movie we reached for all answer we aim to :**
# 
# * **Movies of t s database cover 55 years from 1960 to 2015.**
# * **Most popular movie weighted by voters and rating number is "Interstellar" in 2014.**
# * **Movie with highest adjusted budget is "The Warrior's Way" in 2010 and lowest one is "Love, Wedding, Marriage" in 2011**.
# * **Movie with highest adjusted revenue is "Avatar" in 2009 and lowest one is "Shattered Glass" in 2003.**
# * **Movie with highest adjusted profit is "Star Wars" in 1977 and lowest one is "The Warrior's Way" in 2010.**
# * **Movie with longest runtime is "Carlos" in 2010 and lowest one is "Kid's Story" in 2003.**
# * **Avearage runtime of movies is nearly 109 minutes.**
# * **The year has the highest count release of movies is 2011 with 198 movies in it.**
# * **The year has the highest adjusted profit is 2015 with nearly 17.5 billion Dollar.**
# * **The genre has the most count of released movies is "Drama" with 1755 movies.**
# * **Most star acted in movies is "Robert De Niro" with 52 movies.**
# * **The production company with highest number of released movies is "Universal Pictures" with 329 movies.**
# * **The director who directed maximum Movies is "Steven Spielberg" with 28 movies.**
# 
# ### Limitation
# **limitation in this database from suitable data to analyise that about 35.5% (3853 data rows) only from genuine data with null cells (about 10866 rows), that make our analysis is not free from errors completely.**

# In[32]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




