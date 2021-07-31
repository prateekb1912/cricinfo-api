from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider in process.spiders.list():
    print("Running spider %s" % (spider))
    process.crawl(spider, query = 'dvh')

process.start()