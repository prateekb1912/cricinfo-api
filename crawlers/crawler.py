from typing import Dict
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

class PlayersCrawler(team_info = Dict()):
    def __init__(self):
        self.spider = 'players_spider'

        for info in team_info:
            print(info)



# teams = process.crawl(teams_spider)

# print("HERE HERE", teams)

# # process.crawl(players_spider, team_id = 2)

# print(process.start())

# for spider in process.spiders.list():
#     print("Running spider %s" % (spider))
#     process.crawl(spider, query = 'dvh')