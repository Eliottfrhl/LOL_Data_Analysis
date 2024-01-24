import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

URL = "https://gol.gg/tournament/tournament-matchlist/LEC%20Winter%20Season%202024/"
site_url = "https://gol.gg/"
response = requests.get(URL, headers = headers)
html_content = response.content


soup = BeautifulSoup(html_content, "html.parser")

game_links = soup.find_all('a', title=lambda value : value and 'vs' in value)

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
            print("team matchup : " + h1_elements[i].text.strip())