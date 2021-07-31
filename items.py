# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass

class T20IResultsItem(scrapy.Item):
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    winner = scrapy.Field()
    margin = scrapy.Field()
    venue = scrapy.Field()
    match_date = scrapy.Field()
    match_no = scrapy.Field()

class PlayersItem(scrapy.Item):
    player_id = scrapy.Field()
    full_name = scrapy.Field()
    gender = scrapy.Field()
    role = scrapy.Field()

class MatchResultItem(scrapy.Item):
    id = scrapy.Field()
    info = scrapy.Field()
    state = scrapy.Field()
    status = scrapy.Field()


@dataclass
class PopularTeamsItem:
    team_id: int
    team_name: str
    team_color: str