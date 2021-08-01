from scrapy import spiders
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

#spiders = process.spiders.list()

teams_spider = 'teams_spider'
players_spider = 'players_spider'

# teams = process.crawl(teams_spider)

# print("HERE HERE", teams)

# # process.crawl(players_spider, team_id = 2)

# print(process.start())

# for spider in process.spiders.list():
#     print("Running spider %s" % (spider))
#     process.crawl(spider, query = 'dvh')