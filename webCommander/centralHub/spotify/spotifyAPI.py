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

SPOTIFY_FIXED_ARTIST_CHAR_LEN = 22

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

def get_spotify_artist(artist_name):
    '''
    Authenticate then search an artist based on an artist name. Searches for the name if id is not provided
    '''

    #TODO 
    #Spotify artist is a 22 fixed character ID, but searching for a word would require to first call search_spotify_artist 
    #to get the id which would also return some ids even if not an artist. Not sure how to handle this.

    if len(artist_name) != SPOTIFY_FIXED_ARTIST_CHAR_LEN:
        artist_id = search_spotify_artist(artist_name)

    url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id

    response = requests.get(url, headers=spotify_authenticate())
    return response.text

def search_spotify_artist(artist_name):

    url = SPOTIFY_BASE_URL + SPOTIFY_SEARCH

    params = {
        "q": artist_name,
        "type": "artist"
    }

    response = requests.get(url, headers=spotify_authenticate(), params=params)
    artists_results = json.loads(response.text)

    for artist in artists_results['artists']['items']:
        if artist['name'] == artist_name:
            return artist['id']

def get_artist_albums(artist_name):
    album_dict = {'images':[],
        'name':[],
        'total_tracks':[]}

    if len(artist_name) != SPOTIFY_FIXED_ARTIST_CHAR_LEN:
        artist_id = search_spotify_artist(artist_name)

    url = SPOTIFY_BASE_URL + SPOTIFY_ARTISTS + artist_id + '/albums'

    response = requests.get(url, headers=spotify_authenticate())
    albums_results = json.loads(response.text)

    for album in albums_results['items']:
        album_dict['images'].append(album['images'][0]['url'])
        album_dict['name'].append(album['name'])
        album_dict['total_tracks'].append(album['total_tracks'])

    return album_dict

def main():
    print(get_artist_albums("Taylor Swift"))

if __name__ == '__main__':
    main()