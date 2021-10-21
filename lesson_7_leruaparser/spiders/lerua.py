import scrapy
from scrapy.http import HtmlResponse
from lesson_7_leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo', "//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset")
        return loader.load_item()


        # link = response.url
        # name = response.xpath("//h1/text()").get()
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # photo = response.xpath("//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset").getall()
        #
        # yield AvitoparserItem(link=link, name=name, price=price, photo=photo)
