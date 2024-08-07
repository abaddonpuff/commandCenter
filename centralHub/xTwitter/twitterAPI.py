import os
import json
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv

load_dotenv()

# DEFINE AUTHENTICATION TOKENS
X_AUTHORIZATION_BEARER = os.getenv("X_BEARER_TOKEN")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# DEFINE URLS
X_BASE_URL = "https://api.twitter.com"
X_GET_MYUSER = X_BASE_URL + "/2/users/me"
X_GET_USER = X_BASE_URL + "/2/users/by/username/"
X_TWEET_ID = X_BASE_URL + "/2/tweets/"
X_GET_TWEET = X_BASE_URL + "/2/users/"
X_USAGE = X_BASE_URL + "/2/usage/tweets"

# CODES
TOO_MANY_REQUESTS = 429
SUCCESS = 200


class XUserDoesNotExist(Exception):
    pass


class XAPIUsageExceeded(Exception):
    pass


def x_authenticate():
    return OAuth1Session(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)


def request_to_x_api(endpoint, headers={}, params={}):
    x_session = x_authenticate()
    response = x_session.get(endpoint, headers=headers, params=params)

    print(f"Request to API {response.status_code}")
    if response.status_code == TOO_MANY_REQUESTS:
        raise XAPIUsageExceeded("API Exceeded, try again in 15 Mins")

    return response


def x_userlookup(x_user):
    params = {
        "expansions": "pinned_tweet_id",
        "tweet.fields": "author_id,created_at",
        "user.fields": "created_at,profile_image_url,most_recent_tweet_id",
    }

    api_url = X_GET_USER + x_user

    response = request_to_x_api(api_url, headers={}, params=params)
    data_response = json.loads(response.text)

    if "errors" in data_response.keys():
        raise XUserDoesNotExist(f"No valid response for handle {x_user}")

    return data_response


def get_top_tweets_from_user(x_username, max_results=10):
    # working from username, need to lookup id first
    try:
        x_user_id = x_userlookup(x_username)["data"]["id"]
    except XUserDoesNotExist as e:
        # TODO: better handle this
        print(e)
        return
    params = {
        "max_results": max_results,
        "exclude": "replies,retweets",
        "expansions": "attachments.media_keys,attachments.poll_ids",
        #'since_id': <tweet id num> Option when database is available
        "tweet.fields": "attachments",
        # user.fields: most_recent_tweet_id
    }
    api_url = X_GET_TWEET + x_user_id + "/tweets"

    response = request_to_x_api(api_url, headers={}, params=params)

    tweets = json.loads(response.text)
    return tweets


def get_tweets_since_last(x_user_id: int, last_id: int, max_results=30) -> list:
    params = {
        "max_results": max_results,
        "exclude": "replies,retweets",
        "expansions": "attachments.media_keys,attachments.poll_ids",
        "since_id": last_id,
        "tweet.fields": "attachments",
    }
    api_url = X_GET_TWEET + str(x_user_id) + "/tweets"

    response = request_to_x_api(api_url, headers={}, params=params)

    tweets = json.loads(response.text)
    return tweets


def get_latest_tweet_from_user(x_username):
    try:
        x_user_id = x_userlookup(x_username)["data"]["id"]
    except XUserDoesNotExist as e:
        # TODO: better handle this
        print(e)
        return

    api_url = X_GET_TWEET + x_user_id + "/tweets"

    response = request_to_x_api(api_url, headers={}, params={})

    tweets = json.loads(response.text)
    last_tweet = get_single_tweet(tweets["meta"]["newest_id"])

    return (last_tweet["id"], last_tweet["text"])


def get_single_tweet(tweet_id):
    api_url = X_TWEET_ID + tweet_id
    response = request_to_x_api(api_url, headers={}, params={})

    tweets = json.loads(response.text)
    return tweets["data"]


def main():
    pass


if __name__ == "__main__":
    main()
