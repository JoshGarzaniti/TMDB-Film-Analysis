# -*- coding: utf-8 -*-
"""
Exploratory Analysis of Horror Movies 1970-

Created on Tue Sep  2 17:53:38 2025

@author: Josh Garzaniti
"""

#Packages I'll need
import pandas as pd
import numpy as np
import tmdbsimple as tmdb #use either this or tmdbv3api
import time
import os
from dfply import *
import re
import matplotlib.pyplot as plt

horror_movies = pd.read_csv("G:\My Drive\Personal Projects\horror_movies.csv")

##Exploratory Data Analysis
horror_movies.head(10)    

horror_movies.isna().sum()
#We are ok with having just the NA's in our tagline because that's essentially the movie's
#summary description.

horror_movies.info()
        
horror_movies['title'] = horror_movies['title'].astype(str) 

horror_movies['title'].apply(type).head()

horror_movies['release_date'] = pd.to_datetime(horror_movies['release_date']).dt.date

horror_movies['release_date'].apply(type).head()

horror_movies['tagline'] = horror_movies['tagline'].astype(str) 

horror_movies['tagline'].apply(type).head()

horror_movies['countries'] = horror_movies['countries'].str.extract(r"\['(.+?)'\]")

horror_movies['countries'].head(5)

horror_movies['production_companies'] = (
    horror_movies['production_companies']
    .str.extract(r"\[(.*)\]")[0]
    .str.replace("'", "", regex=False)  
    .str.split(", "))

horror_movies['production_companies'].head(5)

horror_movies['release_date'] = pd.to_datetime(horror_movies['release_date'], errors='coerce')

horror_movies['year'] = horror_movies['release_date'].dt.year

horror_ratings_by_year = horror_movies.groupby('year')['vote_average'].mean()

##Graphing out Average Horror Movie TMDB Ratings since 1970

plt.figure(figsize=(12,6))
plt.plot(horror_ratings_by_year.index, horror_ratings_by_year.values)
plt.title('Average Horror Rating over Time')
plt.xlabel('Year')
plt.ylabel('Average Rating')
plt.show()

##Graphing out Average Horror Movie Budgets by year

horror_with_budget = horror_movies[horror_movies['budget'] > 0]

horror_budgets_by_year = horror_with_budget.groupby('year')['budget'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_budgets_by_year.index, horror_budgets_by_year.values)
plt.title('Average Horror Budget over Time')
plt.xlabel('Year')
plt.ylabel('Average Production Budget')
plt.show()

##Graphing out Horror Revenues by Year

horror_revenues_by_year = horror_movies.groupby('year')['revenue'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_revenues_by_year.index, horror_revenues_by_year.values)
plt.title('Average Horror Revenue over Time')
plt.xlabel('Year')
plt.ylabel('Average Revenue')
plt.show()

##Graphing out Horror Profits by Year

horror_movies['profit'] = horror_movies['revenue'] - horror_movies['budget']

horror_profits_by_year = horror_movies.groupby('year')['profit'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_profits_by_year.index, horror_profits_by_year.values)
plt.title('Average Horror Profit over Time')
plt.xlabel('Year')
plt.ylabel('Average Profit')
plt.show()

##Number of horror movies released each year

horror_movies['release_date'].dt.year.value_counts().sort_index().plot(kind='bar', figsize=(12,6))
plt.title('Number of Horror Movies Released Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()

##Number of profitable horror movies released each year

profitable_horror_movies = horror_movies[horror_movies['profit'] > 0]

profitable_horror_movies['release_date'].dt.year.value_counts().sort_index().plot(kind='bar', figsize=(12,6))
plt.title('Number of Profitable Horror Movies Released Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()
