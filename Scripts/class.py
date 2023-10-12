from json import load
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime


with open('config.json') as f: config = load(f) 
riot_api_key = config['Riot_api_key']

class RiotAPI:
    def __init__(self):
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

class Summoner:
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
    
    def display_stats(self,stat_name,start=0,count=20):
        match_list = self.api.get_match_list_by_puuid(self.puuid,start,count)
        stats = []
        champions = []
        for matchId in match_list:
            game = Match(self.api,matchId)
            performance = game.get_player_performance(self)
            endTimer = game.match_data['info']['gameEndTimestamp']
            stats.append(performance[stat_name])
            champions.append(performance['championName']+' '+str(datetime.datetime.fromtimestamp(endTimer/1000).strftime("%d %H:%M")))
        stats=np.array(stats)
        champions=np.array(champions)
        plt.xticks(rotation = 30)
        plt.bar(champions, stats)
        plt.show()

        


class Match:
    def __init__(self,api,match_id):
        self.api = api
        self.match_id = match_id
        self.match_data = self.api.get_match_by_id(self.match_id)
        
    def get_players(self):
        participants = self.match_data['metadata']['participants']
        players =[]
        for participant in participants:
            players.append(Summoner(api,puuid=participant).summoner_name)
        return players
    
    def get_player_performance(self, player):
        index = next((index for (index, d) in enumerate(self.match_data['info']['participants']) if d["summonerName"] == player.summoner_name), None)
        return self.match_data['info']['participants'][index]
        
    
api = RiotAPI()

Player = Summoner(api,summoner_name='Epsyk')
'''
game = Match(api,Player.get_match_list()[0])

perfo = game.get_player_performance(Player)'''
Player.display_stats('assists')