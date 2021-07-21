"""
    This spider processes JSON requests made by Cricinfo to load the latest scores
    and will store this data in a CSV.
"""

import scrapy
import json
from ..items import MatchResultItem

class LiveScores(scrapy.Spider):
    name = "live_spider"

    start_urls = ['https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?latest=true']

    def parse(self, response):

        match_details = MatchResultItem()

        js = json.loads(response.body)
        matches = js['matches']

        for match in matches:

            # Extract useful information from data 
            match_details['id'] = match['objectId']

            match_details['info'] = match['slug'].replace('-', ' ')
            
            match_details['state'] = match['stage']
            match_details['status'] = match['statusText']

            yield match_details
        

