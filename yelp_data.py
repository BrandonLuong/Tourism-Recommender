import pandas as pd
import requests
import geocoder
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import multiprocessing as mp
import time
from operator import itemgetter
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("YELP_API")
secret = os.getenv("YELP_CLIENT")
def get_businesses(loc):
    url = "https://api.yelp.com/v3/businesses/search"

    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    params = {
        "location": loc,
        ## set radius
        "term": "food",
        "limit": 10
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def fetch_business_details(id):
    """
    Returns list
    """
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews?offset=4&limit=20&sort_by=yelp_sort"

    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    # params = {
    #     "business_id_or_alias": id
    # }
    response = requests.get(url, headers=headers)
    response = response.json()['reviews']

    for d in response:
        d['business_id'] = id
        # alias_list = list(map(itemgetter('alias'), d['categories']))
        # d['categories'] = alias_list
    return response

def fetch_business_details_list(location):
    restaurants = get_businesses(location)
    rest_lst = [fetch_business_details(business['id']) for business in restaurants['businesses']]
    # pd.DataFrame(foo['reviews'])
    return sum(rest_lst, [])
# print(get_businesses("Los Angeles"))