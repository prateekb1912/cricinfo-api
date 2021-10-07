"""
    In this script, we will be extracting the scorecard of a match
"""

import requests
import pandas as pd

# We will use the 52nd match of the IPL 2021 (latest as of now) for sampling purposes
url = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard"\
    "?seriesId=1249214&matchId=1254095"

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

match_id = data['match']['objectId']

