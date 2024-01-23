# Fichier Python pour scrapper les données des matchs d'esport par Games of Legends
# Auteur: Clément Tourte

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
url = "https://gol.gg/tournament/tournament-matchlist/LFL%20Spring%202024/"
match_urls = {}
match_data = {}
i = 1

# Get the content of the div with the specified XPath
response = requests.get(url,headers=headers)
tree = html.fromstring(response.content)

while True:
    Tournament_XPath = "/html/body/div/main/div[2]/div/div[3]/div/section/div/div/table/tbody/tr[" + str(i) + "]/td[1]/a"
    # Use XPath to find the element
    try :
        element = tree.xpath(Tournament_XPath)[0]
        match_url = element.get('href')
        match_urls[element.text] = "https://gol.gg" + match_url[2:]
    except:
        break
    i += 1

for match,match_url in match_urls.items():
    response = requests.get(match_url,headers=headers)
    tree = html.fromstring(response.content)
    match_data[match] = {}
    GameTime_XPath = "/html/body/div"
    GameTime = tree.xpath(GameTime_XPath)[0].text
    match_data[match]["GameTime"] = GameTime

print(match_data)