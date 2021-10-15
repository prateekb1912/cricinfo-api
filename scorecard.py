"""
    In this script, we will be extracting the scorecard of a match
"""

import requests
from utils import *
from datetime import datetime

series_id = 


# We will use the 52nd match of the IPL 2021 (latest as of now) for sampling purposes
url = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard"\
    "?seriesId=1249214&matchId=1254114"

# Create a connection to the database and a cursor object
conn = create_connection('scorecard.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS batters (
    player_id INT PRIMARY KEY,
    batter TEXT,
    runs INTEGER,
    balls INTEGER,
    UNIQUE(player_id, batter, runs, balls) ON CONFLICT IGNORE);""")

c.execute("""
    CREATE TABLE IF NOT EXISTS match_details (
        series_id INT,
        season TEXT,
        match_id INT PRIMARY KEY,
        date TEXT,
        time TEXT,
        ground INT,
        team1 INT,
        team2 INT,
        toss_winner INT,        
        toss_decision TEXT,
        winner INT,
        result TEXT,    
        UNIQUE(match_id) ON CONFLICT REPLACE
        );
""")


response = requests.get(url, headers=headers)

data = response.json()


## Getting all the match details before diving into the batting and bowling scorecards
match_obj = data['match']

match_details = dict()

match_details['series_id'] = match_obj['series']['objectId']
match_details['season'] = match_obj['season']
match_details['match_id'] = match_obj['objectId']

date_time = match_obj['startTime']
d = datetime.fromisoformat(date_time[:-1])

match_details['date'] = d.strftime("%Y-%m-%d")
match_details['time'] = d.strftime("%H-%M-%S")

match_details['ground'] = match_obj['ground']['objectId']
match_details['team1'] = match_obj['teams'][0]['team']['objectId']
match_details['team2'] = match_obj['teams'][1]['team']['objectId']
match_details['toss_winner'] = match_obj['tossWinnerTeamId']
match_details['toss_decision'] = 'bat' if match_obj['tossWinnerChoice'] == 1 else 'bowl'
match_details['winner'] = match_obj['winnerTeamId']
match_details['result'] = match_obj['statusText']


c.execute('''
    INSERT INTO match_details 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', tuple(match_details.values()))


scorecard = data['content']['scorecard']

innings = scorecard['innings']

for inn in innings:
    inn_num = inn['inningNumber']
    team_id = inn['team']['objectId']

    batter_details = []
    batsmen = inn['inningBatsmen']

    for bats in batsmen:
        batter = bats['player']['battingName']
        batter_id = bats['player']['objectId']
        balls_faced = bats['balls']
        runs = bats['runs']
        fours = bats['fours']
        sixes = bats['sixes']
        sr = bats['strikerate']
        mins = bats['minutes']
        if bats['dismissalText'] is not None:
            dismissal_type = bats['dismissalText']['short']
        else:
            break

        batter_details.append({
            'inning': inn_num,
            'team_id': team_id,
            'player_id': batter_id,
            'batter': batter,
            'runs': runs,
            'balls': balls_faced,
            'minutes': mins,
            'fours': fours,
            'sixes': sixes,
            'SR': sr,
            'dismissal_type': dismissal_type
        })

    # for det in batter_details:
    #     c.execute('''INSERT INTO batters VALUES(?,?,?,?)''', 
    #     (det['player_id'], det['batter'], det['runs'], det['balls']))


c.execute('''SELECT * FROM match_details''')
results = c.fetchall()
print(results)

conn.commit()    






        