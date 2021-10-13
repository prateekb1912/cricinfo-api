"""
    This script scrapes the stats records and returns the content IDs for all matches in a series/tournament.
"""

import requests
from bs4 import BeautifulSoup
import re

# We will start with scraping only the franchisee-based T20 leagues and build on it.

header = "https://stats.espncricinfo.com/"


addon = "ci/engine/records/index.html"

page = requests.get(header+addon)
soup = BeautifulSoup(page.content, 'html.parser')

# Finding the specific list with all T20 league titles and IDs 
leagues_list = soup.find_all('ul', attrs={'class': 'Record'})[11]
leagues_links = [{link.text:int(re.findall("[0-9]+",link['href'])[0])} for link in leagues_list.find_all('a')]

for ll in leagues_links:
    league_name = list(ll.keys())[0]
    if league_name == 'ICC Intercontinental Cup':
        continue
    league_id = list(ll.values())[0]
    
    results_link = header+f"ci/engine/records/team/match_results_season.html?id={league_id};type=trophy"
    
    res_page = requests.get(results_link)
    soup = BeautifulSoup(res_page.content, 'html.parser')
    
    recTable = soup.find('table', attrs={'class':'recordsTable'})
    
    season_links = [link['href'] for link in recTable.find_all('a')]

    num_seasons = len(season_links)

    seas_matches = []

    for s in season_links:
        season_page = requests.get(header+s)
        soup = BeautifulSoup(season_page.content, 'html.parser')

        matchTable = soup.find('table', attrs = {'class': 'engineTable'})
        matchLinks = matchTable.find_all('a', string = 'T20')

        matchIDs = [int(re.findall("[0-9]+", link['href'])[0]) for link in matchLinks]

        num_matches = len(matchIDs)
        seas_matches.append(num_matches)
    
    print(seas_matches)
