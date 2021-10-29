# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    follower_username = scrapy.Field()
    full_name = scrapy.Field()
    is_private = scrapy.Field()





