from json import load
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import datetime
import json

with open('config.json') as f: config = load(f) 
riot_api_key = config['Riot_api_key']

class RiotAPI:
    # Classe qui permet de faire les requêtes à l'API Riot, est nécessaire pour les autres classes par la suite
    def __init__(self,riot_api_key):
        self.riot_api_key = riot_api_key
        
    def get_summoner_by_name(self, summoner_name):
        url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + self.riot_api_key
        response = requests.get(url)
        return response.json()
    
    def get_summoner_by_puuid(self,puuid):
        url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' + puuid + '?api_key=' + self.riot_api_key
        response = requests.get(url)
        return response.json()
    
    def get_summoner_by_accountId(self,accountId):
        url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-account/' + accountId + '?api_key=' + self.riot_api_key
        response = requests.get(url)
        return response.json()
    
    def get_match_list_by_puuid(self,puuid,start=0,count=20,gameMode=None):
        assert(gameMode in ['ranked','normal','tourney',None])
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids?start='+str(start)+'&count='+str(count)+'&api_key=' + self.riot_api_key
        if gameMode != None : url += ('&type='+gameMode)
        response = requests.get(url)
        return response.json()
    
    def get_match_by_id(self,match_id):
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/' + match_id + '?api_key=' + self.riot_api_key
        response = requests.get(url)
        return response.json()
    
    def get_match_timeline_by_id(self, match_id):
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/' + match_id + '/timeline/?api_key=' + self.riot_api_key
        response = requests.get(url)
        return response.json()

class Summoner:
    # Classe qui représente un joueur. Elle permet d'accéder à la liste de ses matchs mais également à certaines statistiques globales
    def __init__(self,api,puuid=None,summoner_name=None):
        self.api = api
        if(summoner_name==None and puuid==None):
            raise Exception('You must provide either a summoner name or a puuid')
        elif (summoner_name==None):
            self.summoner_name = api.get_summoner_by_puuid(puuid)['name']
            self.puuid = puuid
        elif (puuid==None):
            self.puuid = api.get_summoner_by_name(summoner_name)['puuid']
            self.summoner_name = summoner_name

    def get_match_list(self,start=0,count=20,gameMode=None):
        match_list = self.api.get_match_list_by_puuid(self.puuid,start,count,gameMode)
        return match_list
    
    def get_kda(self,start=0,count=20):
        match_list = self.api.get_match_list_by_puuid(self.puuid,start,count)
        kda = 0
        for matchId in match_list:
            game = Match(api,match_id=matchId)
            kda += game.get_player_performance(self)['challenges']['kda']
        return kda/len(match_list)
    
    def display_stats(self,stat_name,start=0,count=20,gameMode=None):
        match_list = self.api.get_match_list_by_puuid(self.puuid,start,count,gameMode)
        stats = []
        champions = []
        for matchId in match_list:
            game = Match(self.api,matchId)
            performance = game.get_player_performance(self)
            endTimer = game.match_data['info']['gameEndTimestamp']
            stats.append(60*performance[stat_name]/game.match_data['info']['gameDuration'])
            champions.append(performance['championName']+' '+str(datetime.datetime.fromtimestamp(endTimer/1000).strftime("%d %H:%M")))
        stats=np.array(stats)
        champions=np.array(champions)
        plt.barh(champions, stats)
        plt.show()

        


class Match:
    # Classe qui représente une partie en particulier. Elle permet de stocker les informations sur cette partie et d'en récupérer des statistiques
    def __init__(self,api,match_id):
        self.api = api
        self.match_id = match_id
        self.match_data = self.api.get_match_by_id(self.match_id)
        self.match_timeline = self.api.get_match_timeline_by_id(self.match_id)
        
    def get_players(self):
        participants = self.match_data['metadata']['participants']
        players =[]
        for participant in participants:
            index = self.match_timeline['metadata']['participants'].index(participant)
            dic = {
                "PUUID": participant,
                "summonerName":self.match_data['info']['participants'][index]["summonerName"],
                "InGameID":index+1,
                "Role":self.match_data['info']['participants'][index]["teamPosition"],
                "championName":self.match_data['info']['participants'][index]["championName"],
                "team":self.match_data['info']['participants'][index]["teamId"],
            }
            players.append(dic)
        return players
    
    def get_player_performance(self, player):
        index = next((index for (index, d) in enumerate(self.match_data['info']['participants']) if d["summonerName"] == player.summoner_name), None)
        return self.match_data['info']['participants'][index]
    
    def get_kills(self):
        kills=[]
        for frame in self.match_timeline['info']['frames']:
            for event in frame["events"]:
                if event["type"]=="CHAMPION_KILL":
                    try:
                        dic = {
                            "killer":event["killerId"],
                            "victim":event["victimId"],
                            "timestamp":event["timestamp"],
                            "position":event["position"],
                        }
                    except:
                        print("Pb pour le kill à la frame: " + str(frame))
                    kills.append(dic)
        return kills      