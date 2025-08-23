# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 19:56:19 2025

@author: Josh Garzaniti
"""

#Packages I'll need
import pandas as pd
import numpy as np
import tmdbsimple as tmdb #use either this or tmdbv3api
import time

tmdb.API_KEY = "4ad3aff47fe098b8328804523f23acc2"
#Testing it out on Fight Club (id = 550 on TMDB)
movie_example = tmdb.Movies(550)
example_response = movie_example.info()

print(example_response['title'], example_response['release_date'], example_response['revenue'])

print(example_response['genres'])

print(example_response['release_date'])

#Are Horror Movies Criminally Underrated
#Project Goals

#What I want to do is analyze Horror movies both historically and over the last few years 
#to understand what factors impact their: revenue, vote_average, and vote_count

#Lets start off with that first part. We need to pull all movies with "Horror" as a
#genre.

Horror_Genre_ID_type = 27

Horror_Start_Year = 1970

Horror_End_Year = 2025

horror_movies = []

for year in range(Horror_Start_Year, Horror_End_Year +1):
    page = 1
    while True:
        horror_discover = tmdb.Discover()
        response = horror_discover.movie(
        with_genres=Horror_Genre_ID_type,
        primary_release_date_gte=f"{year}-01-01",
        primary_release_date_lte=f"{year}-12-31",
        sort_by="release_date.asc",
        page=page)
        
        time.sleep(0.5)

    for m in response["results"]:
        details = tmdb.Movies(m["id"]).info()
        horror_movies.append({
                "id": m["id"],
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "vote_average": m.get("vote_average"),
                "vote_count": m.get("vote_count"),
                "budget": details.get("budget"),
                "revenue": details.get("revenue"),
                "runtime": details.get("runtime"),
                "tagline": details.get("tagline"),
                "adult": details.get("adult"),
                "production_companies": [c["name"] for c in details.get("production_companies", [])],
                "countries": [c["name"] for c in details.get("production_countries", [])],
                "language": details.get("original_language"),
            })
        
    if page >= response["total_pages"]:
        break
    page += 1 

horror_movies_df = pd.DataFrame(horror_movies)
print(horror_movies_df.shape)










