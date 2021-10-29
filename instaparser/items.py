# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    user_id = scrapy.Field()
    follower_username = scrapy.Field()
    full_name = scrapy.Field()
    biography = scrapy.Field()
    followers_count = scrapy.Field()
    first_page_posts_count = scrapy.Field()
    non_video_post_count = scrapy.Field()
    posts_like_count = scrapy.Field()
    posts_comment_count = scrapy.Field()
    posts_count = scrapy.Field()
    is_follower = scrapy.Field()
    photo = scrapy.Field()
    following_count = scrapy.Field()






