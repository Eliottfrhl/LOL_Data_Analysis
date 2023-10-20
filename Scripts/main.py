from classes import RiotAPI, Summoner, Match
from json import load, dump

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Tourtipouss")

GameID = Player.get_match_list(gameMode='ranked')

LastGame = Match(API,GameID[0])
