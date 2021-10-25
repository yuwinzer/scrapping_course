from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson_7_leruaparser.spiders.lerua import LeruaSpider
from lesson_7_leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('')
    process.crawl(LeruaSpider, query='зеркало')
    process.start()

