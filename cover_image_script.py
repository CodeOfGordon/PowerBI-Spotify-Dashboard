import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv()


# Data
file_path = "Most Streamed Spotify Songs 2024.csv"
spotify_data = pd.read_csv(file_path, encoding='latin1')

# Client Info
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_access_token(id, secret):
    url = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=header, data=data, auth=(id, secret))
    return response.json()['access_token']      

def get_cover_img_url(track_name, track_artist, token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": f"track:{track_name} artist:{track_artist}", "type": "track", "limit": 1}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get("tracks", {}).get("items", [])
        if items:
            print('img found')
            return items[0]["album"]["images"][0]["url"]  # Largest album cover image URL
    return None


# encoding='ISO-8859-1' since special accented characters are in dataset
df_spotify = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='ISO-8859-1')

token = get_access_token(client_id, client_secret)
spotify_data["Cover URL"] = spotify_data.apply(
    lambda row: get_cover_img_url(row["Track"], row["Artist"], token), axis=1
)

# Save the updated dataset
updated_file_path = "Updated_Spotify_Songs_with_Cover_URLs.csv"
spotify_data.to_csv(updated_file_path, index=False)