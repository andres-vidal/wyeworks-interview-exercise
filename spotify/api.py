from requests import get, post

from utils import request

import json

# Constants

SPOTIFY_API = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNTS_API = "https://accounts.spotify.com/api"

# Load credentials

with open('spotify/credentials.json', 'r') as f:
    credentials = json.load(f)

SPOTIFY_CLIENT_ID = credentials["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = credentials["SPOTIFY_CLIENT_SECRET"]


# Authenticate

response = post(
    f"{SPOTIFY_ACCOUNTS_API}/token",
    auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    data={"grant_type": "client_credentials"}
)

SPOTIFY_ACCESS_TOKEN = response.json()["access_token"]


# API Calls

def get_cover_art(album):

    year, title = album

    target = f"{SPOTIFY_API}/search"

    params = {
        "q": f'album:"{title}" year:{year}',
        "type": "album"
    }

    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }

    response = request(get, target, headers=headers, params=params)
    results = response.json()["albums"]["items"]
    return results[0]["images"][0]["url"] if results else None
