import os
import requests 
import json
import config
import pprint 
from time import sleep   
from requests_oauthlib import OAuth1Session                                                                                                                                                
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

#DEFINE AUTHENTICATION TOKENS
X_AUTHORIZATION_BEARER = os.getenv('X_BEARER_TOKEN')
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

#DEFINE URLS
X_BASE_URL = 'https://api.twitter.com'
X_GET_MYUSER = X_BASE_URL+'/2/users/me'
X_GET_USER = X_BASE_URL+'/2/users/by/username/'
X_TWEET_ID = X_BASE_URL+'/2/tweets/'
X_GET_TWEET = X_BASE_URL+'/2/users/'

#CODES
TOO_MANY_REQUESTS = 429

def x_authenticate():

    return OAuth1Session(
        X_API_KEY,
        X_API_SECRET,
        X_ACCESS_TOKEN,
        X_ACCESS_TOKEN_SECRET
    )

def request_to_x_api(endpoint, headers={}, params={}):
    x_session = x_authenticate()
    response = x_session.get(endpoint, headers=headers, params=params)
    while response.status_code == TOO_MANY_REQUESTS:
        print('Too many requests, trying in 15 mins...')
        sleep(900)
        response = request_to_x_api(api_url, headers={}, params=params)

    return response

def x_userlookup(x_user):

    params = {
        'user.fields': 'created_at',
        'expansions': 'pinned_tweet_id',
        'tweet.fields': 'author_id,created_at',
        'user.fields':'profile_image_url'
    }

    api_url = X_GET_USER + x_user

    response = request_to_x_api(api_url, headers={}, params=params)
    return json.loads(response.text)

def get_all_tweets_from_user(x_username, max_results=10):
    x_user_id = x_userlookup(x_username)['data']['id']

    params = {
        'max_results':max_results
    }
    api_url = X_GET_TWEET + x_user_id + '/tweets'

    response = request_to_x_api(api_url, headers={}, params=params)

    tweets = json.loads(response.text)
    for tweet in tweets['data']:
        print(tweet['id'])
        print(tweet['text'])
    return 

def get_latest_tweet_from_user(x_username):
    x_user_id = x_userlookup(x_username)['data']['id']

    api_url = X_GET_TWEET + x_user_id + '/tweets'

    response = request_to_x_api(api_url, headers={}, params={})

    tweets = json.loads(response.text)
    last_tweet = get_single_tweet(tweets['meta']['newest_id'])

    return (last_tweet['id'],last_tweet['text'])

def get_single_tweet(tweet_id):
    api_url = X_TWEET_ID + tweet_id
    response = request_to_x_api(api_url, headers={}, params={})

    tweets = json.loads(response.text)
    return tweets['data']

def main():
    print(x_userlookup("bbelderbos"))

if __name__ == '__main__':
    main()