import requests
import json

language = "en_US"
version ="13.20.1"

def getChampions(version,language="en_US"):
    url = "http://ddragon.leagueoflegends.com/cdn/"+version+"/data/"+language+"/champion.json"
    response = requests.get(url)

    with open("data/champion.json","w") as file:
        json.dump(response.json(),file)
    
getChampions(version)