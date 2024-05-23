import os
import requests 
import json
import config                      
from requests_oauthlib import OAuth1Session                                                                                                                                                
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv()

#DEFINE AUTHENTICATION TOKENS
X_AUTHORIZATION_BEARER = os.getenv('X_BEARER_TOKEN')
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
#X_AUTHENTICATION_URL = 'https://api.twitter.com/2/oauth2/token'

#DEFINE URLS
X_BASE_URL = 'https://api.twitter.com'
X_GET_MYUSER = '/2/users/me'
X_GET_USER = '/2/users/by/username/'
X_TWEET_ID = 'https://api.twitter.com/2/tweets'


def x_authenticate():

    return OAuth1Session(
        X_API_KEY,
        X_API_SECRET,
        X_ACCESS_TOKEN,
        X_ACCESS_TOKEN_SECRET
    )

def x_userlookup(x_user=None):
    x_session = x_authenticate()


    if x_user == None:
        api_url = X_BASE_URL + X_GET_MYUSER
        return x_session.get(api_url).text

    else:
        api_url = X_BASE_URL + X_GET_USER + x_user
        #Define params
        params = {
            'user.fields': 'created_at',
            'expansions': 'pinned_tweet_id',
            'tweet.fields': 'author_id,created_at'
        }

        response = x_session.get(
            api_url, params=params
        )

    return response.text

def main():
    print(x_userlookup("bbelderbos"))

if __name__ == '__main__':
    main()