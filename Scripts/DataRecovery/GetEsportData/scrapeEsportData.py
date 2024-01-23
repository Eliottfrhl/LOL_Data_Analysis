# Fichier Python pour scrapper les données des matchs d'esport par Games of Legends
# Auteur: Eliott Frohly

# Importation des librairies
import requests
from lxml import html


headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
url = "https://gol.gg/tournament/tournament-matchlist/LFL%20Spring%202023/"
match_urls = {}
match_data = {}
i = 1

# Get the content of the div with the specified XPath
response = requests.get(url,headers=headers)
tree = html.fromstring(response.content)

while True:
    GameLink_XPath = "/html/body/div/main/div[2]/div/div[3]/div/section/div/div/table/tbody/tr[" + str(i) + "]/td[1]/a"
    # Use XPath to find the element
    try :
        GameLinkElement = tree.xpath(GameLink_XPath)[0]
        short_match_url = GameLinkElement.get('href')
        match_url = "https://gol.gg" + short_match_url[2:]
        match_id = match_url.split("/")[5]
        print(match_id)
        match_urls[match_id] = match_url

        Team1_XPath = "/html/body/div/main/div[2]/div/div[3]/div/section/div/div/table/tbody/tr[" + str(i) + "]/td[2]"
        Team1Element = tree.xpath(Team1_XPath)[0]
        Team1 = Team1Element.text
        Team2_XPath = "/html/body/div/main/div[2]/div/div[3]/div/section/div/div/table/tbody/tr[" + str(i) + "]/td[4]"
        Team2Element = tree.xpath(Team2_XPath)[0]
        Team2 = Team2Element.text

        match_data[match_id] = {}
        match_data[match_id]["MatchURL"] = match_url
        match_data[match_id]["Team1"] = Team1
        match_data[match_id]["Team2"] = Team2
    except:
        break
    i += 1


for match_id,match_url in match_urls.items():
    response = requests.get(match_url,headers=headers)
    tree = html.fromstring(response.content)
    
    GameTime_XPath = "/html/body/div/main/div[2]/div/div[3]/div/div/div/div[1]/div/div/div[1]/div[2]/h1"
    GameTime = tree.xpath(GameTime_XPath)[0].text
    match_data[match_id]["GameTime"] = GameTime

