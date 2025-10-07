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

##Remove duplicates from original data
#horror_movies = (
#   horror_movies
#  .drop_duplicates(subset=['title', 'release_year'], keep='first')
#
#    .reset_index(drop=True))
#
#horror_movies


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

horror_movies_cleaned_revenue = horror_movies.dropna(subset=['revenue'])

horror_movies_cleaned_runtime = horror_movies.dropna(subset=['runtime'])

horror_movies_cleaned_ratings = horror_movies.dropna(subset=['vote_average'])

horror_movies_cleaned_profit = horror_movies.dropna(subset=['profit'])

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

#How do Classic Horror Movie Compare to the Field?

# Extract release year
horror_movies['release_year'] = horror_movies['release_date'].dt.year

# Dictionary of originals (title -> release year)
classic_horror_originals = {
    "The Exorcist": 1973,
    "Halloween": 1978,
    "A Nightmare on Elm Street": 1984,
    "Friday the 13th": 1980,
    "The Texas Chain Saw Massacre": 1974,
    "The Shining": 1980,
    "Alien": 1979,
    "Jaws": 1975,
    "The Thing": 1982,
    "Carrie": 1976,
    "Evil Dead": 1981,
    "Child's Play": 1988,
    "Scream": 1996,
    "Candyman": 1992,
    "Poltergeist": 1982,
    "The Silence of the Lambs": 1991,
    "The Conjuring": 2013,
    "It": 2017,      # newer film
    "Hereditary": 2018,
    "Get Out": 2017,
    "The Ring": 2002,
    "Saw": 2004
    }

# Filter by exact (title, year) combo
classic_horror_df = (
    horror_movies[
        horror_movies.apply(
            lambda row: classic_horror_originals.get(row['title']) == row['release_year'],
            axis=1
            )
    ][['title', 'release_date', 'release_year',
       'vote_average', 'vote_count', 'budget', 'revenue', 'profit', 'runtime']]
    .sort_values(by='release_date')
    .reset_index(drop=True))

classic_horror_df = (
    classic_horror_df
    .drop_duplicates(subset=['title', 'release_year'], keep='first')
    .reset_index(drop=True))

classic_horror_df

# %%
# Now that we have the classic horror movies, let's compare their average metrics
# to the overall averages for horror movies

overall_average_df = pd.DataFrame({
    'Metric': ['vote_average', 
               'vote_count', 
               'budget', 
               'revenue',
               'profit',
               'profit pct of budget',],
    'Overall Average': [
        horror_movies['vote_average'].mean(),
        horror_movies['vote_count'].mean(),
        horror_movies['budget'].mean(),
        horror_movies['revenue'].mean(),
        (horror_movies['revenue'] - horror_movies['budget']).mean(),
        (horror_movies['profit'] / horror_movies['budget']).mean()
    ]   
})
classic_horror_averages = {
    'Metric': ['vote_average', 
               'vote_count', 
               'budget', 
               'revenue',
               'profit',
               'profit pct of budget',],
    'Classic Horror Average': [
        classic_horror_df['vote_average'].mean(),
        classic_horror_df['vote_count'].mean(),
        classic_horror_df['budget'].mean(),
        classic_horror_df['revenue'].mean(),
        classic_horror_df['profit'].mean(),
        (classic_horror_df['profit'] / classic_horror_df['budget']).mean()
    ]
}
classic_horror_average_df = pd.DataFrame(classic_horror_averages)

comparison_df = pd.merge(overall_average_df, classic_horror_average_df, on='Metric')

comparison_df['Difference'] = comparison_df['Classic Horror Average'] - comparison_df['Overall Average']

comparison_df['Percent Difference'] = (comparison_df['Difference'] / comparison_df['Overall Average']) * 100


comparison_df.style.format({
    'Overall Average': '{:,.2f}',
    'Classic Horror Average': '{:,.2f}',
    'Difference': '{:,.2f}',
    'Percent Difference': '{:,.2f}%',
})

# %%
#Graphing average votes between overall horror movies and classics
vote_labels = ['All Horror Movies', 'Cult Classic Horror Movies']

vote_averages = [
    comparison_df.loc[comparison_df['Metric'] == 'vote_average', 'Overall Average'].values[0],
    comparison_df.loc[comparison_df['Metric'] == 'vote_average', 'Classic Horror Average'].values[0]
]

x = np.arange(len(vote_labels))
plt.figure(figsize=(8,6))
bars = plt.bar(x, vote_averages, color=['blue', 'orange'])


for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2., 
        height,
        f'{height:.2f}',
        ha='center', va='bottom'
    )

plt.xticks(x, vote_labels)
plt.ylabel('Average TMDB Rating (0-10 scale)')
plt.title('Average review rating for Horror Movies\ncompared to Cult Classics',
          fontsize=14, weight='bold')
plt.show()


# %%
#Graphing average vote counts between overall horror movies and classics

vote_count_labels = ['All Horror Movies', 'Cult Classic Horror Movies']

vote_count_averages = [
    comparison_df.loc[comparison_df['Metric'] == 'vote_count', 'Overall Average'].values[0],
    comparison_df.loc[comparison_df['Metric'] == 'vote_count', 'Classic Horror Average'].values[0]
]

x = np.arange(len(vote_count_labels))
plt.figure(figsize=(8,6))
bars = plt.bar(x, vote_count_averages, color=['blue', 'orange'])


for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2., 
        height,
        f'{height:.2f}',
        ha='center', va='bottom'
    )

plt.xticks(x, vote_labels)
plt.ylabel('Average Votes on TMDB')
plt.title('Average number of reviews of Horror Movies\ncompared to Cult Classics',
          fontsize=14, weight='bold')
plt.show()

# %%
#Graphing comparison between classic and overall budgets

budget_labels = ['All Horror Movies', 'Cult Classic Horror Movies']

budget_averages = [
    comparison_df.loc[comparison_df['Metric'] == 'budget', 'Overall Average'].values[0],
    comparison_df.loc[comparison_df['Metric'] == 'budget', 'Classic Horror Average'].values[0]
]

x = np.arange(len(budget_labels))
plt.figure(figsize=(8,6))
bars = plt.bar(x, budget_averages, color=['blue', 'orange'])


for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        height,
        f'{height/1e6:.2f}M',
        ha='center', va='bottom'
    )

plt.xticks(x, budget_labels)
plt.ylabel('Production Budget (USD)')

# Format y-axis ticks in millions
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x*1e-6:.1f}M'))

plt.title('Average Production Budget of Horror Movies\ncompared to Cult Classics',
          fontsize=14, weight='bold')
plt.show()


# %%

revenue_labels = ['All Horror Movies', 'Cult Classic Horror Movies']

revenue_averages = [
    comparison_df.loc[comparison_df['Metric'] == 'revenue', 'Overall Average'].values[0],
    comparison_df.loc[comparison_df['Metric'] == 'revenue', 'Classic Horror Average'].values[0]
]

x = np.arange(len(revenue_labels))
plt.figure(figsize=(8,6))
bars = plt.bar(x, revenue_averages, color=['blue', 'orange'])


for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        height,
        f'{height/1e6:.2f}M',
        ha='center', va='bottom'
    )

plt.xticks(x, revenue_labels)
plt.ylabel('Box Office Grossings (USD)')

# Format y-axis ticks in millions
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x*1e-6:.1f}M'))

plt.title('Average Box Office Grossings of Horror Movies\ncompared to Cult Classics',
          fontsize=14, weight='bold')
plt.show()

# %%

#Graphing comparison between classic and overall profits

profit_labels = ['All Horror Movies', 'Cult Classic Horror Movies']

profit_averages = [
    comparison_df.loc[comparison_df['Metric'] == 'profit', 'Overall Average'].values[0],
    comparison_df.loc[comparison_df['Metric'] == 'profit', 'Classic Horror Average'].values[0]
]

x = np.arange(len(profit_labels))
plt.figure(figsize=(8,6))   
bars = plt.bar(x, profit_averages, color=['blue', 'orange'])


for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        height,
        f'{height/1e6:.2f}M',
        ha='center', va='bottom'
    )

plt.xticks(x, profit_labels)
plt.ylabel('Profit (USD)')

# Format y-axis ticks in millions
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x*1e-6:.1f}M'))

plt.title('Average Profit of Horror Movies\ncompared to Cult Classics',
          fontsize=14, weight='bold')
plt.show()

# %%

overall_row = pd.DataFrame([{
    'title': 'Overall Horror Average',
    'release_date': pd.NaT,
    'release_year': None,
    'vote_average': horror_movies_cleaned_ratings['vote_average'].mean(),
    'vote_count': horror_movies_cleaned_votes['vote_count'].mean(),
    'budget': horror_movies_cleaned_budget['budget'].mean(),
    'revenue': horror_movies_cleaned_revenue['revenue'].mean(),
    'profit': horror_movies_cleaned_profit['profit'].mean(),
    'runtime': horror_movies_cleaned_runtime['runtime'].mean()
}])

classics_vs_overall = pd.concat([classic_horror_df, overall_row], ignore_index=True)

classics_vs_overall['profit_pct_of_budget'] = classics_vs_overall['profit'] / classics_vs_overall['budget'] * 100

classics_vs_overall = classics_vs_overall.round(1)

classics_vs_overall

# %%

# Now I want to plot out all of these metrics for each of the
# classic movies as well as the overall average

plt.figure(figsize=(12,6))

scatter = plt.scatter(
    classics_vs_overall['title'], 
    classics_vs_overall['vote_average'],
    c=classics_vs_overall['vote_average'],
    cmap='coolwarm',    
    s=100,       
    edgecolor='black')

cbar = plt.colorbar(scatter)
cbar.set_label('Vote Average', rotation=270, labelpad=15)

plt.axhline(
    y=overall_row['vote_average'].values[0], 
    color='blue', linestyle='--', label='Overall Average')

plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel('Average Rating (0–10 scale)')
plt.title('Average Ratings of Classic Horror Movies vs Overall Average', fontsize=14, weight='bold')
plt.tight_layout()
plt.show()


# %%