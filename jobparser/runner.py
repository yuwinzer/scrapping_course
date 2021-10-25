from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
from pymongo import MongoClient

# clean DB before start
client = MongoClient('localhost', 27017)
mongo_base = client.vacancy1110
hhru = mongo_base.hhru
hhru.delete_many({})
sjru = mongo_base.sjru
sjru.delete_many({})

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()