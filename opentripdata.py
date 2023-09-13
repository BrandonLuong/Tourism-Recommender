import asyncio
import aiohttp
import pandas as pd

key = "5ae2e3f221c38a28845f05b6206760d37e97518692bd93fe307403b9"
async def fetch_geoname(session, destination):
    base_url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {
        "apikey": key,
        "name": destination
    }
    async with session.get(base_url, params=params) as response:
        data = await response.json()
        return data

async def fetch_xid(session, xid):
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey=5ae2e3f221c38a28845f05b6206760d37e97518692bd93fe307403b9"
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data['wikipedia_extracts']['text']
        except:
            return "No Description"

async def fetch_attractions(session, lat, lon):
    base_url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": key,
        "lat": lat,
        "lon": lon,
        "radius": 10000,
        "limit": 100,
        "kinds": "amusements,interesting_places,sport,transport,shops",
        "rate": 3
    }
    async with session.get(base_url, params=params) as response:
        data = await response.json()
        return data['features']

async def main(dest):
    async with aiohttp.ClientSession() as session:
        destination = await fetch_geoname(session, dest)
        lat, lon = destination['lat'], destination['lon']
        attractions = await fetch_attractions(session, lat, lon)
        
        tasks = [fetch_xid(session, attraction['properties']['xid']) for attraction in attractions]
        descriptions = await asyncio.gather(*tasks)
        
        df = pd.DataFrame([{
            "name": attraction['properties']['name'],
            "rate": attraction['properties']['rate'],
            "kinds": attraction['properties']['kinds'],
            "desc": description
        } for attraction, description in zip(attractions, descriptions)])
        
        return df

# async def main_async(dest):
#     dest_df = await main(dest)
#     return dest_df

# if __name__ == "__main__":
# foo = asyncio.run(main('Los Angeles'))
# print(foo)
    