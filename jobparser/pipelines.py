# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1110

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            new_item = {}
            print(item)
            # item['salary_min'], item['salary_max'], item['currency'] = None, None, None
            item['salary'] = self.process_salary(item['salary'])
            new_item['name'] = item['name']
            new_item['salary_min'] = item['salary'][0]
            new_item['salary_max'] = item['salary'][1]
            new_item['currency'] = item['salary'][2]
            new_item['link'] = item['link']
            print(new_item)
            collection = self.mongo_base[spider.name]
            collection.insert_one(new_item)
            return item



    def process_salary(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        if len(salary) == 5:
            print('enter with len=5')
            if salary[0] == 'от ':
                salary_min = int(salary[1].replace('\xa0', ''))
                salary_max = None
                currency = salary[3]
            elif salary[0] == 'до ':
                salary_min = None
                salary_max = int(salary[1].replace('\xa0', ''))
                currency = salary[3]
        elif len(salary) == 7:
            salary_min = int(salary[1].replace('\xa0', ''))
            salary_max = int(salary[3].replace('\xa0', ''))
            currency = salary[5]
        return [salary_min, salary_max, currency]



