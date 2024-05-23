import os
import requests 
import json
import config                      
from requests_oauthlib import OAuth1Session                                                                                                                                                
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

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

def get_spotify_artist(artist_name=None):
    '''
    Authenticate then search an artist based on an artist name. Searches for the name if id is not provided
    '''

    if artist_name is None:
        print('No artist id provided (Error handling)')
    else:
        if len(artist_name) != 22:
            artist_id = search_spotify_artist(artist_name)

        headers = spotify_authenticate()

        url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id
        response = requests.get(url, headers=headers)
        return response.text

def search_spotify_artist(artist_name=None):

    url = SPOTIFY_BASE_URL + SPOTIFY_SEARCH

    if artist_name is None:
        print('No artist name provided (Error handling)')
    else:
        headers = spotify_authenticate()

        params = {
            "q": artist_name,
            "type": "artist"
        }

        response = requests.get(url, headers=headers, params=params)
        artists_results = json.loads(response.text)

        for artist in artists_results['artists']['items']:
            if artist['name'] == artist_name:
                return artist['id']

def main():
    print(get_spotify_artist("Taylor Swift"))

if __name__ == '__main__':
    main()