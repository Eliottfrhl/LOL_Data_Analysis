from classes import RiotAPI, Summoner, Match
from json import load, dump
from copy import deepcopy


def MatchUp(API,Player,count=20,roleAdverse="SAME"):
    # Liste les MatchUps de ce joueur sur les count dernières parties
    info = ["championName","kills","deaths","assists"]
    lst = Player.get_match_list(gameMode="ranked",count=count)

    MatchUps = []

    for match_id in lst:
        Game = Match(API,match_id)
        MatchUp = {}
        playerPerformance = Game.get_player_performance(Player)
        MatchUp["win"] = playerPerformance["win"]
        if roleAdverse=="SAME":role = playerPerformance["teamPosition"]
        for participant in Game.match_data["info"]["participants"]:
            if participant["summonerName"] == Player.summoner_name:
                MatchUp["p1"]={
                    "summoner": participant["summonerName"],
                    "champion":participant["championName"],
                    "kills":participant["kills"],
                    "deaths":participant["deaths"],
                    "assists":participant["assists"],
                    "role":role,
                }
            elif participant["teamPosition"] == role:
                MatchUp["p2"]={
                    "summoner": participant["summonerName"],
                    "champion":participant["championName"],
                    "kills":participant["kills"],
                    "deaths":participant["deaths"],
                    "assists":participant["assists"],
                    "role":role,
                }
        MatchUps.append(MatchUp)
    return(MatchUps)

def MatchUpWinrate(MatchUps):
    # Retourne un dictionnaire de <nombre de champions> dictionnaires, chacun de taille <nombre de champions> indiquant les statistiques du matchup entre le champion de p1 et les autres
    with open("data/champions.json",encoding="utf-8") as f:
        champ_js = load(f)

    champs = {}

    for champ in champ_js.keys():
        champs[champ_js[champ]["name"]] = {
            "win_count":0,
            "loss_count":0,
        }
        
    results = {}

    for champ in champ_js.keys():
        results[champ_js[champ]["name"]] = deepcopy(champs)

    for MatchUp in MatchUps:
        if MatchUp["win"]==True:
            results[MatchUp["p1"]["champion"]][MatchUp["p2"]["champion"]]["win_count"]+=1
        else:
            results[MatchUp["p1"]["champion"]][MatchUp["p2"]["champion"]]["loss_count"]+=1

    for key1 in results.keys():
        for key2 in results[key1].keys():
            if results[key1][key2]["win_count"]+results[key1][key2]["loss_count"] !=0:
                results[key1][key2]["winrate"]=(results[key1][key2]["win_count"])/(results[key1][key2]["win_count"]+results[key1][key2]["loss_count"])
    return results


def SoloKill(Game,Player):
    # Liste les solokill entre le joueur et son vis à vis, dans les 2 sens, lors d'une partie
    timeline = Game.match_timeline
    players = Game.get_players()
    p1index = next((index for (index, d) in enumerate(players) if d["summonerName"] == Player.summoner_name), None)
    p1=players[p1index]
    for player in players:
        if player["Role"]==p1["Role"] and player["PUUID"]!=p1["PUUID"]:p2=player
    SoloKill = []
    SoloKilled = []
    SoloKill_count = 0
    SoloKilled_count = 0
    for frame in timeline["info"]["frames"]:
        for event in frame["events"]:
            if event["type"]=="CHAMPION_KILL" and event["victimId"]==p2["InGameID"] and event["killerId"]==p1["InGameID"] and 'assistingParticipantIds' not in event.keys():
                SoloKill_count += 1
                SoloKill.append(event)
            elif event["type"]=="CHAMPION_KILL" and event["victimId"]==p1["InGameID"] and event["killerId"]==p2["InGameID"] and 'assistingParticipantIds' not in event.keys():
                SoloKilled_count += 1
                SoloKilled.append(event)
    dic ={
        "p1":p1,
        "p2":p2,
        "SoloKill": SoloKill,
        "SoloKillCount": SoloKill_count,
        "SoloKilled": SoloKilled,
        "SoloKilledCount": SoloKilled_count 
    }
    return dic

def StatsMoy(API, Player, count=20,gameMode='ranked'):
    stats ={
       "kill":0,
       "assist" :0,
       "death" :0,
       "solokill":0,
       "solokilled":0,
    }
    matchList = Player.get_match_list(gameMode,count=count)
    for ID in matchList:
        Game = Match(API,ID)
        idx = next((index for (index, d) in enumerate(Game.match_data['info']['participants']) if d["summonerName"] == Player.summoner_name), None)
        stats["kill"] += Game.match_data["info"]["participants"][idx]["kills"]
        stats["assist"] += Game.match_data["info"]["participants"][idx]["assists"]
        stats["death"] += Game.match_data["info"]["participants"][idx]["deaths"]
        SK = SoloKill(Game,Player)
        stats["solokill"]+=SK["SoloKillCount"]
        stats["solokilled"]+=SK["SoloKilledCount"]
    for key in stats.keys():
        stats[key]=stats[key]/count
    return stats