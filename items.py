# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class T20IResultsItem(scrapy.Item):
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    winner = scrapy.Field()
    margin = scrapy.Field()
    venue = scrapy.Field()
    match_date = scrapy.Field()
    match_no = scrapy.Field()

class TeamRosterInfoItem(scrapy.Item):
    team = scrapy.Field()
    squadSize = scrapy.Field()

class PlayersItem(scrapy.Item):
    name = scrapy.Field()