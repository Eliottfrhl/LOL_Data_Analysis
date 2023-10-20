from classes import RiotAPI, Summoner, Match
from json import load, dump


def MatchUp(API,Player):
    info = ["championName","kills","deaths","assists"]
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
    return(MatchUps)



def SoloKill(Game,Player):
    timeline = Game.match_timeline
    players = Game.get_players()
    p1index = next((index for (index, d) in enumerate(players) if d["summonerName"] == Player.summoner_name), None)
    p1=players[p1index]
    for player in players:
        if player["Role"]==p1["Role"] and player["PUUID"]!=p1["PUUID"]:p2=player
    print(p1["summonerName"]+" and "+p2["summonerName"])
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