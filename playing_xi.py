"""
    In this script, we will be extracting the playing XIs for the teams playing in a match
"""

import requests
import pandas as pd

# We will use the 1st ever CPL match to begin our data extraction
url = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/team-players?"\
    "&seriesId=1249214&matchId=1254099"

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

match_date = data['match']['startDate']
match_id = data['match']['objectId']

# Getting to the level where both teams' players are recorded 
players = data['content']['matchPlayers']['teamPlayers']

team1 = players[0]
team2 = players[1]

teams = [team1, team2]

# Get all required details for both teams
team1_id = team1['team']['objectId']
team1_name = team1['team']['longName']

team2_id = team2['team']['objectId']
team2_name = team2['team']['longName']

team_names = [team1_name, team2_name]

teams_plyr_list = []

i = 0
for team in teams:
    temp_list = []
    position = 1
    for player in team['players']:
        # Retrieve relevant details for each player like palying role, is captain/wicket-keeper, 
        # batting and bowling styles, nationality (for T20 leagues)

        curr_plyr_details = dict()

        curr_plyr_details['match_id'] = match_id
        curr_plyr_details['team'] = team_names[i]

        curr_plyr_details['position'] = position
        
        position += 1

        curr_plyr_details['role_type'] = player['playerRoleType']
        
        player = player['player']
        
        curr_plyr_details['name'] = player['name']
        curr_plyr_details['playing_role'] = player['playingRole']
        curr_plyr_details['batting_style'] = player['battingStyles'][0]
        if len(player['bowlingStyles']):
            curr_plyr_details['bowling_style'] = player['bowlingStyles'][0]
        else:
            curr_plyr_details['bowling_style'] = None

        curr_plyr_details['country_id'] = player['countryTeamId']

        temp_list.append(curr_plyr_details)

    i += 1

    teams_plyr_list.append(temp_list)

# Now that we have the data, we will now convert it into a DataFrame which 
# will store it as a csv file 

team1 = pd.DataFrame(teams_plyr_list[0])
team2 = pd.DataFrame(teams_plyr_list[1])

playing_xi_data = pd.concat([team1, team2], axis=0, ignore_index=True)

print(playing_xi_data)