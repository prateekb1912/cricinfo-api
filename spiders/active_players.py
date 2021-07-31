"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy
import json
from ..items import PlayersItem

class PlayersSpider(scrapy.Spider):
    name = "players_spider"
    
    start_urls = ["https://hs-consumer-api.espncricinfo.com/v1/pages/player/search"
    "?mode=BOTH&page=1&records=10&filterTeamId=1"
    "&filterFormatLevel=INTERNATIONAL&filterActive=true"]
    
    def parse(self, response):
        details = json.loads(response.body)

        playersItem = PlayersItem() 

        for player in details['results']:
            playersItem['player_id'] = (player['objectId'])
            playersItem['full_name'] = (player['longName'])
            playersItem['gender'] = player['gender']
            playersItem['role'] = player['playingRole']

            yield playersItem
