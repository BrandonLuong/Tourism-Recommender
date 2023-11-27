import pandas as pd
import requests
import geocoder
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import multiprocessing as mp
import time
import concurrent.futures
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

api_key = os.getenv("OPENTRIP_API")
# Want: 
# assume that the user already has an idea of what area they want to hit. Ex: southern california instead of the united states
# keep the criteria small, reduce the complexity 
# idea: "please enter a major city:"
## keep a dictionary/list of countries, if the search is too wide, spit out a message ("please narrow your search")

# question: what should the area criteria be?
## major cities. ex: san diego, new york
## prefectures. ex: tokyo, osaka

## criteria: by municipality (rather than country)
## have a criteria for each region/continent. ex: US -> states -> cities, japan -> prefecture
## use openstreetmaps api to get the type of location (city, country, town, etc) for narrowing the search criteria

# give a one day itinerary

# feature_class = 'A'
# g = geocoder.geonames('Japan', key='imcheesed')
# print(g.description)
# print(g.json)


# functions to get activities in desired destination
# should return a list/dictionary
# output: attraction, attraction type,
# content based filtering
# create a user profile:
## rate how much a type of attraction interests you

# using opentrip map to get attractions and its information

def get_geoname(destination):
    """
    Function to get geographic coordinates for the given destination
    """
    base_url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {
        "apikey": api_key,
        "name": destination
    }
    response = requests.get(base_url, params=params).json()
    return response

def get_lat_lon(geoname):
    return geoname['lat'], geoname['lon']

def get_attractions(lat, lon):
    # point instead of radius (?)
    base_url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": api_key,
        "lat": lat,
        "lon": lon,
        "radius": 10000,   # Radius (in meters) to search for attractions around the destination
        "limit": 100,      # Adjust this number to get more or fewer attractions
        "kinds": "amusements,interesting_places,sport,transport,shops",
        "rate": 3
    }

    response = requests.get(base_url, params=params)
    # data = response.json()

    # if "error" in data:
    #     print(f"Error occurred: {data['error']['message']}")
    #     return []

    # attractions = data["features"]
    return response.json()

def get_xid(x):
    """
    Function to get detailed information about a place
    """
    url = "https://api.opentripmap.com/0.1/en/places/xid/" + x + f"?apikey={api_key}"
    response = requests.get(url)
    try:
        return response.json()['wikipedia_extracts']['text']
    except:
        return "No Description"


def get_attraction_info(attraction):
    xid = attraction['properties']['xid']
    desc = get_xid(xid)
    return {
        "name": attraction['properties']['name'],
        "rate": attraction['properties']['rate'],
        "kinds": attraction['properties']['kinds'],
        "desc": desc
    }
def get_attraction_df(dest):
    """
    Function to create a pandas dataframe of nearby places for a given destination
    """
    destination = get_geoname(dest)
    latitude, longitude = get_lat_lon(destination)
    attractions = get_attractions(latitude, longitude)

    attractions_list = attractions['features']

    # with mp.Pool(5) as pool:
    # with concurrent.futures.ProcessPoolExecutor() as executer:
    #     attractions_info = executer.map(get_attraction_info, attractions_list)

    # df = pd.DataFrame(attractions_info)
    # return attractions_info
    return attractions_list
    
    # df = pd.json_normalize(attractions_list)
    # df['desc'] = df['properties.xid'].apply(get_xid)
    # return df[["properties.name", "properties.rate", "properties.kinds", "desc"]]

# print(get_attraction_df('Los Angeles'))

## implement collaborative filtering and content based filtering

## content based filtering (TFIDF)

# async def main():
#     attract_list = get_attraction_df("Los Angeles")
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for attraction in attract_list:
#             task = asyncio.ensure_future(get_attract_data, attract_list['id'])

# async def get_attract_data(session, attraction):


# def tfidf_model(df):
#     preproc_df = df.set_index("properties.name")
#     return preproc_df

# if __name__ == "__main__":
#     st = time.time()
#     attraction_df = get_attraction_df('Los Angeles')
#     print(attraction_df)

#     et = time.time()
#     elapsed_time = et - st
#     print('Execution time:', elapsed_time, 'seconds')
