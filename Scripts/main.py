from classes import RiotAPI, Summoner, Match
from json import load, dump
import playerVisualization as pv
import gameVisualization as gv

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Tourtipouss")

Matchlist = Player.get_match_list(gameMode='ranked')

Lastgame = Match(API,Matchlist[0])

output = gv.golddiffmin(Lastgame)

print(output)