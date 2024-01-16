# Data Analysis project on League of Legends

Ce projet a pour objectif de nous familiariser avec l'API Riot et plus largement l'analyse et le traitement de données.

## Utilisation

Le fichier demo.ipynb regroupe quelques fonctionnalités développées et les présente de manière plus didactique que les fichiers Python. N'hésitez pas à y faire un tour pour vous familiariser avec notre système.

## Structure

### class.py

Regroupe les classes Riot API, Summoner et Match.

### getData.py

Récupère les données des champions pour les stocker localement.

### playerVisualization.py

Ensemble de fonctions retournant des données et des statistiques concernant un joueur.

### gameVisualization.py

Ensemble de fonctions retournant des données et des statistiques concernant un match.

## Classes

### Riot API

Permet de récupérer des matchs, des joueurs ou des informations sur le jeu.

### Summoner

Permet de récupérer les derniers matchs de ce joueur, ainsi que diverses informations.

### Match

Permet de récupérer les informations d'un match.

# Collaboration

### En début de session de travail
- `git pull origin main`
- `pip install -r requirements.txt`

Quand tu as fini quelque chose,
- `pip freeze > requirements.txt`
- Add dans VSCode ou `git add {nom du fichier}`
- `git commit -m "Message"`
- `git push origin main`

# Ressources

- [Medium de Xenesis](https://medium.com/@benjamin.castet)
- [Games Of Legends, base de données de games compétitives](https://gol.gg/esports/home/)
- [Cassiopeia, Python Framework for LoL](https://github.com/meraki-analytics/cassiopeia)
- [Page de ressources](https://github.com/FloPrm/lol_analytics)
