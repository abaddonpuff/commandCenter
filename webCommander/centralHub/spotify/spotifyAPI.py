import os
from typing import NamedTuple
import requests
import json
import config
import pprint
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from collections import defaultdict


load_dotenv()

#DEFINE AUTHENTICATION TOKENS
SPOTIFY_API_KEY = os.getenv('SPOTIFY_CLIENTID')
SPOTIFY_API_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

#DEFINE URLS
SPOTIFY_BASE_AUTH_URL = 'https://accounts.spotify.com'
SPOTIFY_BASE_URL = 'https://api.spotify.com'
SPOTIFY_AUTH = '/api/token'
SPOTIFY_ARTISTS = '/v1/artists/'
SPOTIFY_SEARCH = '/v1/search'


class Album(NamedTuple):
    name: str
    image: str
    total_tracks: int


class SpotifyArtistDoesNotExist(Exception):
    pass

def spotify_authenticate():
    '''
    Obtains the authentication bearer for a user. And returns the Bearer authorization header
    '''

    auth_url = SPOTIFY_BASE_AUTH_URL + SPOTIFY_AUTH
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
    "grant_type": "client_credentials",
    "client_id": SPOTIFY_API_KEY,
    "client_secret": SPOTIFY_API_SECRET
    }

    response = requests.post(auth_url, headers=headers, data=data)
    token_info = json.loads(response.text)
    token = token_info['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def get_spotify_artist_by_id(artist_id):
    '''
    Authenticate then search an artist based on an artist name. Searches for the name if id is not provided
    '''

    url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id

    response = requests.get(url, headers=spotify_authenticate())
    return response.text

def get_spotify_artist(artist_name):
    '''
    Authenticate then search an artist based on an artist name. Searches for the name if id is not provided
    '''

    artist_id = search_spotify_artist_by_name(artist_name)
    print(artist_id)

    url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id[3]

    response = requests.get(url, headers=spotify_authenticate())
    return response.text

def search_spotify_artist_by_name(artist_name):
    url = SPOTIFY_BASE_URL + SPOTIFY_SEARCH

    params = {
        "q": artist_name,
        "type": "artist"
    }

    response = requests.get(url, headers=spotify_authenticate(), params=params)
    artists_results = json.loads(response.text)

    for artist in artists_results['artists']['items']:
        if artist['name'] == artist_name:
            name = artist['name']
            popularity = artist['popularity']
            artist_id = artist['id']
            if len(artist['images']) > 0:
                album_image = artist['images'][0]['url']
            else:
                album_image = "N/A"
    return (name,album_image,popularity,artist_id)

def search_spotify_artist(artist_name):
    '''
    Obtains all possible artists based on a name, user to select the right name to add.
    '''
    results = []

    url = SPOTIFY_BASE_URL + SPOTIFY_SEARCH

    params = {
        "q": artist_name,
        "type": "artist"
    }

    response = requests.get(url, headers=spotify_authenticate(), params=params)
    artists_results = json.loads(response.text)

    for artist in artists_results['artists']['items']:
        name = artist['name']
        popularity = artist['popularity']
        artist_id = artist['id']
        if len(artist['images']) > 0:
            album_image = artist['images'][0]['url']
        else:
            album_image = "N/A"
        results.append((name,album_image,popularity,artist_id))

    return results


def get_artist_albums(artist_name: str) -> list[Album]:
    artist_id = search_spotify_artist_by_name(artist_name)

    url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id[3] + '/albums'

    response = requests.get(url, headers=spotify_authenticate())
    albums_results = json.loads(response.text)

    albums = []
    for album in albums_results['items']:
        albums.append(
            Album(
                name=album['name'],
                image=album['images'][0]['url'],
                total_tracks=album['total_tracks']
            )
        )
    return albums

def main():
    pprint.pprint(get_artist_albums("Taylor Swift"))

if __name__ == '__main__':
    main()
