"""
    In this script, we will be extracting the playing XIs for the teams playing in a match
"""

import requests
import bs4
import json

# We will use the 1st ever CPL match to begin our data extraction
url = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/team-players?lang=en&seriesId=604578&matchId=635215"

headers = {
  'authority': 'hs-consumer-api.espncricinfo.com',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36',
  'accept': '*/*',
  'sec-gpc': '1',
  'origin': 'https://www.espncricinfo.com',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.espncricinfo.com/',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

response = requests.get(url, headers=headers)

data = response.json()

# Getting to the level where both teams' players are recorded 
players = data['content']['matchPlayers']['teamPlayers']

team1 = players[0]
team2 = players[1]

# Get all required details for both teams
team1_id = team1['team']['objectId']
team1_name = team1['team']['longName']

team2_id = team2['team']['objectId']
team2_name = team2['team']['longName']


# Retrieve relevant details for each player like palying role, 