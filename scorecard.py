"""
    In this script, we will be extracting the scorecard of a match
"""

import requests
from utils import *


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
        team1_id INT,
        team2_id INT,
        toss_winner INT,        
        toss_decision TEXT,
        winner INT,
        result TEXT,
        player_of_match TEXT,
    );
""")


response = requests.get(url, headers=headers)

data = response.json()

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


c.execute('''SELECT batter, runs, balls FROM batters WHERE (runs/balls) >= 1''')
results = c.fetchall()
print(results)

conn.commit()    






        