import requests
from bs4 import BeautifulSoup

URL = "https://gol.gg/tournament/tournament-matchlist/LEC%20Winter%20Season%202024/"
site_url = "https://gol.gg/"
response = requests.get(URL)
html_content = response.content


soup = BeautifulSoup(html_content, "html.parser")

game_links = soup.find_all('a', title=lambda value : value and 'vs' in value)

for link in game_links:
    match_link = site_url + link.get('href')[3:]

    match_response = requests.get(match_link)
    match_html_content = match_response.content

    match_soup = BeautifulSoup(match_html_content, "html.parser")

    h1_element = match_soup.find('h1')
    if h1_element:
        print(h1_element.text.strip())
    


#retrieve <h1>
