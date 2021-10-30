# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
from pymongo import MongoClient


class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram_followers


    def process_item(self, item, spider):
        item['likes_per_post_average'] = 0
        item['comments_per_post_average'] = 0
        if item['first_page_posts_count'] != 0:
            item['likes_per_post_average'] = item['posts_like_count'] / item['first_page_posts_count']
            item['comments_per_post_average'] = item['posts_comment_count'] / item['first_page_posts_count']
        del item['first_page_posts_count']
        del item['posts_like_count']
        del item['posts_comment_count']
        # print('очистили данные ')


        if self.item_is_good_enough(item) == True:
            if item['is_follower'] == True:
                collection = self.mongo_base[f"{item['username']}_followers"]
                collection.insert_one(item)
                print(f"залито в followers {item['username']}")
            else:
                collection = self.mongo_base[f"{item['username']}_followings"]
                collection.insert_one(item)

        return item

    def item_is_good_enough(self, item):
        if item['posts_count'] > 12 and item['followers_count'] > 30:
            print('норм')
            return True
        else:
            print(f"отсеян: {item['posts_count']}, {item['followers_count']}")
            return False


