# -*- coding: utf-8 -*-
"""
Exploratory Analysis of Horror Movies 1970-

Created on Tue Sep  2 17:53:38 2025

@author: Josh Garzaniti
"""

# %%
# Imports & setup
import pandas as pd
import numpy as np
import tmdbsimple as tmdb
import time, os, re
from dfply import *
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# %%
# Load Data
horror_movies = pd.read_csv("C:/Personal Projects/horror_movies.csv")

# %%
# Quick exploration
horror_movies.head(10)
horror_movies.isna().sum()
horror_movies.info()


# %%
# Data cleaning / formatting
horror_movies['title'] = horror_movies['title'].astype(str)
horror_movies['release_date'] = pd.to_datetime(horror_movies['release_date'], errors='coerce')
horror_movies['year'] = horror_movies['release_date'].dt.year
horror_movies['tagline'] = horror_movies['tagline'].astype(str)
horror_movies['countries'] = horror_movies['countries'].str.extract(r"\['(.+?)'\]")

horror_movies['production_companies'] = (
    horror_movies['production_companies']
    .str.extract(r"\[(.*)\]")[0]
    .str.replace("'", "", regex=False)
    .str.split(", ")
)

horror_movies.head()


horror_movies['release_date'] = pd.to_datetime(horror_movies['release_date'], errors='coerce')

horror_movies['year'] = horror_movies['release_date'].dt.year

# %%
# Ratings over time
horror_ratings_by_year = horror_movies.groupby('year')['vote_average'].mean()
plt.figure(figsize=(12,6))
plt.plot(horror_ratings_by_year.index, horror_ratings_by_year.values)
plt.title('Average Horror TMDB Rating over Time')
plt.xlabel('Year')
plt.ylabel('Average Rating (0-10 scale)')
plt.show()


# %%
# Budgets over time
horror_with_budget = horror_movies[horror_movies['budget'] > 0]
horror_budgets_by_year = horror_with_budget.groupby('year')['budget'].mean()
plt.figure(figsize=(12,6))
plt.plot(horror_budgets_by_year.index, horror_budgets_by_year.values)
plt.title('Average Horror Budget over Time')
plt.xlabel('Year')
plt.ylabel('Average Production Budget')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
plt.show()


# %%
#Revenue over Time
horror_revenues_by_year = horror_movies.groupby('year')['revenue'].mean()
plt.figure(figsize=(12,6))
plt.plot(horror_revenues_by_year.index, horror_revenues_by_year.values)
plt.title('Average Horror Revenue over Time')
plt.xlabel('Year')
plt.ylabel('Average Revenue')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}')) 
plt.show()

# %%
#Profit by Year
horror_movies['profit'] = horror_movies['revenue'] - horror_movies['budget']
horror_profits_by_year = horror_movies.groupby('year')['profit'].mean()
plt.figure(figsize=(12,6))
plt.plot(horror_profits_by_year.index, horror_profits_by_year.values)
plt.title('Average Horror Profit over Time')
plt.xlabel('Year')
plt.ylabel('Average Profit')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}')) 
plt.show()

# %%
#Movies Each Year
horror_movies['release_date'].dt.year.value_counts().sort_index().plot(kind='bar', figsize=(12,6))
plt.title('Number of Horror Movies Released Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()

# %%
#Profitable Movies each Year
profitable_horror_movies = horror_movies[horror_movies['profit'] > 0]
profitable_horror_movies['release_date'].dt.year.value_counts().sort_index().plot(kind='bar', figsize=(12,6))
plt.title('Number of Profitable Horror Movies Released Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()

# %%
#Percentage of Profitable Movies Each Year
profitable_horror_movies['release_date'].dt.year.value_counts().sort_index() / horror_movies['release_date'].dt.year.value_counts().sort_index() * 100
(100 * profitable_horror_movies['release_date'].dt.year.value_counts().sort_index() / horror_movies['release_date'].dt.year.value_counts().sort_index()).plot(kind='bar', figsize=(12,6))
plt.title('Percentage of Profitable Horror Movies Each Year')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
plt.show()

# %%
# Production companies
all_production_companies = horror_movies['production_companies'].explode()
top_10_horror_producers = all_production_companies.value_counts().head(10)
print(top_10_horror_producers)

Horror_movies_by_production_company = all_production_companies.value_counts()
Horror_movies_by_company_bar_plot = Horror_movies_by_production_company.head(10).plot(kind='bar', figsize=(12,6))
plt.title('Top 10 Horror Producers since 1970')
plt.xlabel('Production Company')
plt.ylabel('Number of Horror Films Produced')
plt.show()


# %%
# Ratings by production company
horror_movies_exploded = horror_movies.explode('production_companies')
average_rating_by_company = (
    horror_movies_exploded
    .groupby('production_companies')
    .agg({'vote_average': 'mean', 'title': 'count'})
    .rename(columns={'title': 'movie_count'})
    .reset_index()
)

average_rating_by_company_filtered = average_rating_by_company[average_rating_by_company['movie_count'] >= 25]
top_10_companies_by_rating = average_rating_by_company_filtered.sort_values(by='vote_average', ascending=False).head(10)

print(top_10_companies_by_rating)

# --- Plot with decimals + labels ---
ax = top_10_companies_by_rating.set_index('production_companies')['vote_average'].plot(
    kind='bar', figsize=(12,6), color='orange'
)

plt.title('Top 10 Production Companies by Average Horror Movie TMDB Rating')
plt.suptitle('for companies with at least 25 horror movies')
plt.xlabel('Company')
plt.ylabel('Average Rating (0-10 scale)')

# Add labels on bars with 1 decimal place
plt.bar_label(ax.containers[0], fmt="%.1f", padding=3)

plt.show()


# %%
# Replace 0s with NaN in the specified columns
horror_movies[['vote_average','vote_count', 'budget', 'revenue', 'runtime', ]] = horror_movies[['vote_average','vote_count', 'budget', 'revenue', 'runtime', ]].replace(0, np.nan)

# Then drop rows with NA in these key columns (if you want a cleaned dataset)
horror_movies_cleaned_all = horror_movies.dropna(subset=['vote_count', 'budget', 'revenue', 'vote_average', 'runtime'])

horror_movies_cleaned_votes = horror_movies.dropna(subset=['vote_count'])

horror_movies_cleaned_budget = horror_movies.dropna(subset=['budget'])

horror_movies_cleaned_runtime = horror_movies.dropna(subset=['runtime'])

# %%
#Correlation analysis cleaned runtime

horror_cleaned_runtime_correlation_matrix = horror_movies_cleaned_runtime[['vote_average', 'vote_count', 'budget', 'revenue', 'profit', 'runtime']].corr()

horror_cleaned_runtime_correlation_matrix.style.background_gradient(cmap='coolwarm')

#There's a moderately high positive correlation between vote count and revenue
#as well as vote count and budget. There's also a very high positive
#correlation between revenue and profit, which is expected.
#budget also has a moderate positive correlation with vote count and revenue.
#It looks like there's a negative correlation between runtime and
#vote average (but it's weak)
# %%