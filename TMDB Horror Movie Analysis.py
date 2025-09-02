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









