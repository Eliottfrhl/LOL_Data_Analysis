from classes import RiotAPI, Summoner, Match
from json import load, dump
import playerVisualization as pv
import gameVisualization as gv

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Epsyk")

GameID = Player.get_match_list(gameMode='ranked')

LastGame = Match(API,GameID[0])

with open("data/champions.json",encoding="utf-8") as f:
    champ_js = load(f)

champs = {}

for champ in champ_js:
    champs[champ["name"]] = {
        "win_count":0,
        "loss_count":0,
    }
    
results = {}

for champ in champ_js:
    results[champ["name"]] = champs

MatchUps=pv.MatchUp(API,Player)

for MatchUp in MatchUps:
    if MatchUp["win"]==True:
        results[MatchUp["p1"]["champion"]][MatchUp["p2"]["champion"]]["win_count"]+=1
    else:
        results[MatchUp["p1"]["champion"]][MatchUp["p2"]["champion"]]["loss_count"]+=1

for key1 in results.keys():
    for key2 in results[key1].keys():
        results[key1][key2]["winrate"]=(results[key1][key2]["winrate"])/(results[key1][key2]["win"]+results[key1][key2]["loss"])

print(results["Rakan"])