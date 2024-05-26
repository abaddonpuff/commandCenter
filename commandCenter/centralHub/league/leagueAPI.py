import os
import requests 
import json
import config                      
from requests_oauthlib import OAuth1Session                                                                                                                                                
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

#DEFINE AUTHENTICATION TOKENS
LEAGUE_API_KEY = os.getenv('LEAGUE_API_KEY')

#DEFINE URLS
LEAGUE_BASE = 'https://americas.api.riotgames.com'
LEAGUE_BY_RIOTID = '/riot/account/v1/accounts/by-riot-id/'
LEAGUE_GAMES_BY_SUMMONER = '/lol/match/v5/matches/by-puuid/'

def get_league_summoner(summoner, tag_id):
    '''
    Gets the Summoner ID by name and tag
    '''
    url = LEAGUE_BASE + LEAGUE_BY_RIOTID + summoner + '/' + tag_id

    headers ={
        'Accept-Language':"en-US,en;q=0.9,es;q=0.8",
        'Accept-Charset':"application/x-www-form-urlencoded; charset=UTF-8",
        'X-Riot-Token':LEAGUE_API_KEY
    }
    # params = {
    #     'api_key':LEAGUE_API_KEY
    # }
    results = json.loads(requests.get(url, headers=headers).text)

    return results['puuid']

def get_league_games_by_summoner_name(summoner, tag_id, start_time=0, endtime=0, count=20):
    '''
    Gets games played by a specific user by name and tag with optional start_time, endtime
    and amount of results.
    '''
    puuid = get_league_summoner(summoner, tag_id)
    url = LEAGUE_BASE + LEAGUE_GAMES_BY_SUMMONER + puuid + '/ids'

    headers={
        'Accept-Language':"en-US,en;q=0.9,es;q=0.8",
        'Accept-Charset':"application/x-www-form-urlencoded; charset=UTF-8",
        'X-Riot-Token':LEAGUE_API_KEY
    }

    params={
        'start':start_time,
        'count':count
    }

    results = requests.get(url, headers=headers, params=params)

    return results.text

def main():
    print(get_league_games_by_summoner_name(summoner="Dr Alu", tag_id="NA1"))

if __name__ == '__main__':
    main()