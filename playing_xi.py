"""
    In this script, we will be scraping out the playing XI for the two teams which will 
    be taking part in the game. We will then store it in a csv file for further use.
"""

import requests
import bs4 
import uncurl


# We will be using the first CPL match to get our project started
match_url = """https://stats.espncricinfo.com/ci/engine/match/635215.html/match-playing-xi"""


resp = requests.get(match_url)

print(resp)