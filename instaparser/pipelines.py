# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram


    def process_item(self, item, spider):
        self.count_average(item)
        if self.item_is_good_enough(item) == True:
            if item['is_follower'] == True:
                collection = self.mongo_base[f"{item['username']}_followers"]
                try:
                    collection.insert_one(item)
                except dke:
                    pass
                print(f"залито в followers {item['username']}")
            else:
                collection = self.mongo_base[f"{item['username']}_followings"]
                try:
                    collection.insert_one(item)
                except dke:
                    pass
                print(f"залито в followings {item['username']}")
        return item

    def item_is_good_enough(self, item):
        # here we check a "quality" of parsed user. If he has posts and followers count big enough he is good.
        # But need users with mentioning "doll" and "bjd" hashtags his posts descriptions
        if item['posts_count'] > 12 and item['followers_count'] > 30:
            print(f"Проходит. P:{item['posts_count']}, F-r: {item['followers_count']}, F-g:{item['following_count']}")
            str_text = ' '.join(item['posts_text'])
            if 'doll' in str_text or 'bjd' in str_text:
                print(f"есть doll или bjd в текстах!")
                return True
            else:
                print(f"но нет нужных хэштегов")
                return False
        else:
            print(f"Отсеян. P:{item['posts_count']}, F-r: {item['followers_count']}, F-g:{item['following_count']}")
            return False

    def count_average(self, item):
        item['likes_per_post_average'] = 0
        item['comments_per_post_average'] = 0
        if item['first_page_posts_count'] != 0:
            item['likes_per_post_average'] = int(round(item['posts_like_count'] / item['first_page_posts_count']))
            item['comments_per_post_average'] = int(round(item['posts_comment_count'] / item['first_page_posts_count']))
        del item['first_page_posts_count']
        del item['posts_like_count']
        del item['posts_comment_count']
        return item


