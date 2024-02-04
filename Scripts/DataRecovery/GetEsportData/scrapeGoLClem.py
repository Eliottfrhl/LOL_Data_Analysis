import requests
from bs4 import BeautifulSoup
import json

class LEC:
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
        self.team_mapping = {"MAD": "MDK"}  # Add any other mappings as needed

    def get_common_name(self, team_name):
        return self.team_mapping.get(team_name, team_name)

    def retrieve_team_data(self):
        matchlist_response = requests.get(self.tournament_url, headers=self.headers)
        matchlist_content = matchlist_response.content
        matchlist_soup = BeautifulSoup(matchlist_content, "html.parser")

        team_name_selector = 'td.text-left > a'
        team_elements = matchlist_soup.select(team_name_selector)

        # Extract unique team names from the list of matches
        matches = [team_element.text.strip() for team_element in team_elements]
        unique_teams = set()

        for match in matches:
            team_names = match.split(" vs ")
            unique_teams.update(team_names)

        # Create a dictionary with unique team names and match information
        self.LEC_DATA = {team: {"TeamName": team, "Matches": {}} for team in unique_teams if team != "MAD"}

        # Store information about each match for each team
        for match in matches:
            team_names = match.split(" vs ")
            common_names = [self.get_common_name(team) for team in team_names]
            for team, common_name in zip(team_names, common_names):
                if common_name != "MAD":  # Exclude MAD
                    if match not in self.LEC_DATA[common_name]["Matches"]:
                        self.LEC_DATA[common_name]["Matches"][match] = {"info": f"Information about {match}"}

    def storeData(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.LEC_DATA, outfile, indent=4)

# Usage example
LEC_WINTER_23 = LEC("https://gol.gg/tournament/tournament-matchlist/LEC%20Winter%20Season%202024/")
LEC_WINTER_23.retrieve_team_data()
LEC_WINTER_23.storeData("LEC_WINTER_23.json")
