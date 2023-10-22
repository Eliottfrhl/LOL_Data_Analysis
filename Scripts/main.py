from classes import RiotAPI, Summoner, Match
from json import load, dump
import playerVisualization as pv
import gameVisualization as gv

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Epsyk")

print("Retrieving last MatchUps")
mu1 = pv.LastMatchUps(API,Player,count=100)
print("Establishing all MatchUps winrate")
mu2 = pv.MatchUpWinrate(mu1)

print(pv.BestMatchUps(mu2,"Nautilus"))