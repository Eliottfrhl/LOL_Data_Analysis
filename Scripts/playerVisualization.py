from classes import RiotAPI, Summoner, Match
from json import load


def Matchup(Player):
    return True

with open('config.json') as f: config = load(f) 
key = config['Riot_api_key']
  
API = RiotAPI(key)    

Player = Summoner(API, summoner_name="Tourtipouss")

lst = Player.get_match_list(gameMode="ranked",count=5)

print(lst)
MatchUps = []

for match_id in lst:
    Game = Match(API,match_id)
    MatchUp = {}
    playerPerformance = Game.get_player_performance(Player)
    role = playerPerformance["teamPosition"]
    MatchUp["role"]=role
    for participant in Game.match_data["info"]["participants"]:
        if participant["teamPosition"] == role:
            if participant["summonerName"] == Player.summoner_name:
                MatchUp["p1"]={
                    "summoner": participant["summonerName"],
                    "champion":participant["championName"],
                    "kills":participant["kills"],
                    "deaths":participant["deaths"],
                    "assists":participant["assists"]
                }
            else:
                MatchUp["p2"]={
                    "summoner": participant["summonerName"],
                    "champion":participant["championName"],
                    "kills":participant["kills"],
                    "deaths":participant["deaths"],
                    "assists":participant["assists"]
                }
    MatchUps.append(MatchUp)
    
print(MatchUps)

            


