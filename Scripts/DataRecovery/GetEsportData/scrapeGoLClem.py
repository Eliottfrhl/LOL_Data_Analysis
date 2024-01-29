import requests
from bs4 import BeautifulSoup
import json

headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

matchlist_URL = "https://gol.gg/tournament/tournament-matchlist/LEC%20Winter%20Season%202024/"
ranking_URL = "https://gol.gg/tournament/tournament-ranking/LEC%20Winter%20Season%202024/"
site_url = "https://gol.gg/"

class LEC :
    def __init__(self, tournament_url, headers=None):
        self.tournament_url = tournament_url
        self.headers = headers = {
            'authority': 'www.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            }
        self.LEC_DATA = {}

    def retrieve_team_data(self):
        team_response = requests.get(self.tournament_url, headers=self.headers)
        team_content = team_response.content
        team_soup = BeautifulSoup(team_content, "html.parser")

        team_name_selector = 'body > div > main > div:nth-child(7) > div > div:nth-child(5) > div > section > div > div > table > tbody > tr > td.footable-visible.footable-first-column > a'

        team_elements = team_soup.select(team_name_selector)

        for team_element in team_elements:
            team_name = team_element.text.strip()
            print(team_name)
            self.LEC_DATA[team_name] = {"TeamName": team_name}
 
    
    def storeData(self, filename):
            with open(filename, 'w') as outfile:
                json.dump(self.LEC_DATA, outfile, indent=4)

LEC_WINTER_23 = LEC(ranking_URL)
LEC_WINTER_23.retrieve_team_data()
LEC_WINTER_23.storeData("LEC_WINTER_23.json")

"""game_links = soup.find_all('a', title=lambda value : value and 'vs' in value)

for link in game_links:
    match_link = site_url + link.get('href')[3:]

    match_response = requests.get(match_link, headers=headers)
    match_html_content = match_response.content

    match_soup = BeautifulSoup(match_html_content, "html.parser")

    h1_elements = match_soup.find_all('h1')

    for i in range(len(h1_elements)):
        gametime_bool = ":" in h1_elements[i].text.strip()
        if gametime_bool:
           print("matchtime : " + h1_elements[i].text.strip())
        else:
            print("team matchup : " + h1_elements[i].text.strip())"""