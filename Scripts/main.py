from classes import RiotAPI, Summoner, Match
from json import load, dump
from playerVisualization import MatchUp

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Tourtipouss")

GameID = Player.get_match_list(gameMode='ranked')

LastGame = Match(API,GameID[0])

timeline = LastGame.match_timeline
lst = []

for frame in timeline["info"]["frames"]:
    for event in frame["events"]:
        if event["type"]=="CHAMPION_KILL" and :
            