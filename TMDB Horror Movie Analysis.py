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
import matplotlib.ticker as mtick

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
plt.title('Average Horror TMDBRating over Time')
plt.xlabel('Year')
plt.ylabel('Average Rating (0-10 scale)')
plt.show()

##Graphing out Average Horror Movie Budgets by year

horror_with_budget = horror_movies[horror_movies['budget'] > 0]

horror_budgets_by_year = horror_with_budget.groupby('year')['budget'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_budgets_by_year.index, horror_budgets_by_year.values)
plt.title('Average Horror Budget over Time')
plt.xlabel('Year')
plt.ylabel('Average Production Budget')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}')) 
plt.show()

##Graphing out Horror Revenues by Year

horror_revenues_by_year = horror_movies.groupby('year')['revenue'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_revenues_by_year.index, horror_revenues_by_year.values)
plt.title('Average Horror Revenue over Time')
plt.xlabel('Year')
plt.ylabel('Average Revenue')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}')) 
plt.show()

##Graphing out Horror Profits by Year

horror_movies['profit'] = horror_movies['revenue'] - horror_movies['budget']

horror_profits_by_year = horror_movies.groupby('year')['profit'].mean()

plt.figure(figsize=(12,6))
plt.plot(horror_profits_by_year.index, horror_profits_by_year.values)
plt.title('Average Horror Profit over Time')
plt.xlabel('Year')
plt.ylabel('Average Profit')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}')) 
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

##Percentage of profitable horror movies each year

profitable_horror_movies['release_date'].dt.year.value_counts().sort_index() / horror_movies['release_date'].dt.year.value_counts().sort_index() * 100

(100 * profitable_horror_movies['release_date'].dt.year.value_counts().sort_index() / horror_movies['release_date'].dt.year.value_counts().sort_index()).plot(kind='bar', figsize=(12,6))
plt.title('Percentage of Profitable Horror Movies Each Year')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

plt.show()

##Who Produces Horror the Most?

all_production_companies = horror_movies['production_companies'].explode()

top_10_horror_producers = all_production_companies.value_counts().head(10)

print(top_10_horror_producers)

Horror_movies_by_production_company = all_production_companies.value_counts()

Horror_movies_by_company_bar_plot = Horror_movies_by_production_company.head(10).plot(kind='bar', figsize=(12,6))
plt.title('Top 10 Horror Producers since 1970')
plt.xlabel('Production Company')
plt.ylabel('Number of Horror Films Produced')
plt.show()

##Average Rating by Production Company (For companies with at least 25 horror movies)

horror_movies_exploded = horror_movies.explode('production_companies')
average_rating_by_company = (
    horror_movies_exploded
    .groupby('production_companies')
    .agg({'vote_average': 'mean', 'title': 'count'})
    .rename(columns={'title': 'movie_count'})
    .reset_index())
average_rating_by_company_filtered = average_rating_by_company[average_rating_by_company['movie_count'] >= 25]
top_10_companies_by_rating = average_rating_by_company_filtered.sort_values(by='vote_average', ascending=False).head(10)
print(top_10_companies_by_rating)

top_10_companies_by_rating_plot = top_10_companies_by_rating.set_index('production_companies')['vote_average'].plot(kind='bar', figsize=(12,6))
plt.title('Top 10 Production Companies by Average Horror Movie TMDB Rating')
plt.suptitle('for companies with at least 25 horror movies')
plt.xlabel('Company')
plt.ylabel('Average Rating (0-10 scale)')
plt.show()