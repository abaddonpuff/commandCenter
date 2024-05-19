import os
import requests 
import json
import config                      
from requests_oauthlib import OAuth1Session                                                                                                                                                
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv()

X_AUTHORIZATION_BEARER = os.getenv('X_BEARER_TOKEN')

X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')

X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

X_USERNAME_URL = 'https://api.twitter.com/2/users/me'
X_TWEET_ID = 'https://api.twitter.com/2/tweets'
X_AUTHENTICATION_URL = 'https://api.twitter.com/2/oauth2/token'

def x_authentication(url):
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'code':'VGNibzFWSWREZm01bjN1N3dicWlNUG1oa2xRRVNNdmVHelJGY2hPWGxNd2dxOjE2MjIxNjA4MjU4MjU6MToxOmFjOjE',
    'grant_type': 'authorization_code',
    'client_id': X_CLIENTID,
    'client_secret': X_CLIENT_SECRET,
    'redirect_uri': 'https://127.0.0.1',
    'code_verifier':'challenge'
    }

    response = requests.post(url, headers=headers)
    print(response.text)

def x_authentication_authbearer():

    oauth = OAuth1Session(
        X_API_KEY,
        X_API_SECRET,
        X_ACCESS_TOKEN,
        X_ACCESS_TOKEN_SECRET
    )

    params = {
    'usernames': '0xAbadd0n',
    'user.fields': 'created_at',
    'expansions': 'pinned_tweet_id',
    'tweet.fields': 'author_id,created_at'
    }

    user_url= X_USERNAME_URL

    response = oauth.get(
        user_url
    )


    print(response.text)

def main():
    x_authentication_authbearer()

if __name__ == '__main__':
    main()