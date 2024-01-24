import requests
from lxml import html
import json

LFL_23_URL = "https://gol.gg/tournament/tournament-matchlist/LFL%20Spring%202023/"


class Tournament:
    def __init__(self, tournament_url):
        self.tournament_url = tournament_url
        self.headers = {
            'authority': 'www.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }    
        self.tournament_data = {}
    
    def retrieveTournamentData(self):
        i = 1

        response = requests.get(self.tournament_url,headers=self.headers)
        tree = html.fromstring(response.content)

        while True:
            GameLink_XPath = "/html/body/div/main/div[2]/div/div[3]/div/section/div/div/table/tbody/tr[" + str(i) + "]/td[1]/a"

            try :
                GameLinkElement = tree.xpath(GameLink_XPath)[0]
                short_match_url = GameLinkElement.get('href')
                match_url = "https://gol.gg" + short_match_url[2:]
                match_id = match_url.split("/")[5]
                self.tournament_data[match_id] = {}
                self.tournament_data[match_id]["MatchURL"] = match_url
            except:
                break

            i += 1

    def retrieveMatchData(self, match_id):
        response = requests.get(self.tournament_data[match_id]["MatchURL"],headers=self.headers)
        tree = html.fromstring(response.content)
        
        GameTime_XPath = "/html/body/div/main/div[2]/div/div[3]/div/div/div/div[1]/div/div/div[1]/div[2]/h1"
        GameTime = tree.xpath(GameTime_XPath)[0].text
        self.tournament_data[match_id]["GameTime"] = GameTime

        Teams_XPath = "/html/body/div/main/div[2]/div/h1"
        Teams = tree.xpath(Teams_XPath)[0].text
        Team1, Team2 = Teams.split(" vs ")
        self.tournament_data[match_id][Team1] = {"Side":"Blue", "Players":{}}
        self.tournament_data[match_id][Team2] = {"Side":"Red", "Players":{}}

        for i,Position in enumerate(["Top", "Jungle", "Mid", "ADC", "Support"]):
            RoleBlue_XPath = "/html/body/div/main/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/table/tbody/tr["+str(i+1)
            PlayerBlue_Data = {}

            RoleRed_XPath = "/html/body/div/main/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div[2]/table/tbody/tr["+str(i+1)
            PlayerRed_Data = {}

            ChampionBlue_XPath = RoleBlue_XPath + "]/td[1]/a[1]/img"
            print(ChampionBlue_XPath)
            ChampionBlue = tree.xpath(ChampionBlue_XPath)[0].get('alt')
            PlayerBlue_Data["Champion"] = ChampionBlue

            ChampionRed_XPath = RoleRed_XPath + "]/td[1]/a[1]/img"
            ChampionRed = tree.xpath(ChampionRed_XPath)[0].get('alt')
            PlayerRed_Data["Champion"] = ChampionRed

            PlayerBlue_XPath = RoleBlue_XPath + "]/td[1]/a[2]"
            PlayerBlue = tree.xpath(PlayerBlue_XPath)[0].text
            PlayerBlue_Data["Player"] = PlayerBlue

            PlayerRed_XPath = RoleRed_XPath + "]/td[1]/a[2]"
            PlayerRed = tree.xpath(PlayerRed_XPath)[0].text
            PlayerRed_Data["Player"] = PlayerRed

            KDABlue_XPath = RoleBlue_XPath + "]/td[3]"
            KDABlue = tree.xpath(KDABlue_XPath)[0].text
            PlayerBlue_Data["KDA"] = KDABlue
            
            KDARed_XPath = RoleRed_XPath + "]/td[3]"
            KDARed = tree.xpath(KDARed_XPath)[0].text
            PlayerRed_Data["KDA"] = KDARed

            self.tournament_data[match_id][Team1]["Players"][Position] = PlayerBlue_Data
            self.tournament_data[match_id][Team2]["Players"][Position] = PlayerRed_Data

    def retrieveAllMatchData(self):
        for match_id in self.tournament_data:
            self.retrieveMatchData(match_id)

LFL23 = Tournament(LFL_23_URL)
LFL23.retrieveTournamentData()
LFL23.retrieveAllMatchData()
with open('LFL23.json', 'w') as outfile:
    json.dump(LFL23.tournament_data, outfile, indent=4)