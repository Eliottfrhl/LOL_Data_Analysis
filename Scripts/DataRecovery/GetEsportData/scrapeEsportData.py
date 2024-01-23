# Fichier Python pour scrapper les données des matchs d'esport par Games of Legends
# Auteur: Clément Tourte

# Importation des librairies
import requests
from lxml import html

url = "https://gol.gg/tournament/tournament-matchlist/LFL%20Spring%202024/"
match_urls = {}
match_data = {}
i = 1

# Get the content of the div with the specified XPath
response = requests.get(url)
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
    response = requests.get(match_url)
    print(response.text)
    tree = html.fromstring(response.content)
    match_data[match] = {}
    GameTime_XPath = "/html/body/div"
    print(tree.xpath(GameTime_XPath))
    print(match)
    print(match_url)
    GameTime = tree.xpath(GameTime_XPath)[0].text
    match_data[match]["GameTime"] = GameTime

print(match_data)