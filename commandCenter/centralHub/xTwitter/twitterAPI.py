import os
import requests                                                                                                                                                                                                     
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv()

X_AUTHORIZATION_BEARER = os.getenv('X_BEARER_TOKEN')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
X_USERNAME_URL = 'https://api.twitter.com/2/users/by/username/'
X_AUTHENTICATION_URL = 'https://api.twitter.com/2/oauth2/token'

def x_authentication(url):
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'code':'VGNibzFWSWREZm01bjN1N3dicWlNUG1oa2xRRVNNdmVHelJGY2hPWGxNd2dxOjE2MjIxNjA4MjU4MjU6MToxOmFjOjE',
    'grant_type': 'authorization_code',
    'client_id': X_ACCESS_TOKEN,
    'client_secret': X_ACCESS_TOKEN_SECRET,
    'redirect_uri': 'https://www.example.com',
    'code_verifier':'challenge'
    }

    response = requests.post(url, headers=headers)
    print(response.text)

def main():
    x_authentication(X_AUTHENTICATION_URL)

if __name__ == '__main__':
    main()