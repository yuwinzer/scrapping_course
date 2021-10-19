# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1110

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            new_item = {}
            # print(item)  # debug
            item['salary'] = self.process_salary_hhru(item['salary'])
            new_item['name'] = item['name']
            new_item['salary_min'] = item['salary'][0]
            new_item['salary_max'] = item['salary'][1]
            new_item['currency'] = item['salary'][2]
            new_item['link'] = item['link']
            # print(new_item)  # debug
            collection = self.mongo_base[spider.name]
            collection.insert_one(new_item)
            return item

        if spider.name == 'sjru':
            new_item = {}
            # print(item)  # debug
            item['salary'] = self.process_salary_sjru(item['salary'])
            new_item['name'] = item['name']
            new_item['salary_min'] = item['salary'][0]
            new_item['salary_max'] = item['salary'][1]
            new_item['currency'] = item['salary'][2]
            new_item['link'] = item['link']
            # print(new_item)  # debug
            collection = self.mongo_base[spider.name]
            collection.insert_one(new_item)
            return item



    def process_salary_sjru(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        # print(salary)  # debug
        if len(salary) == 4:

            if salary[0] == 'от':
                temp_salary = salary[2].replace('\xa0', '')
                temp_salary = temp_salary.replace('руб.', '')
                salary_min = int(temp_salary)
                salary_max = None
                currency = 'руб.'
            elif salary[0] == 'до':
                salary_min = None
                temp_salary = salary[2].replace('\xa0', '')
                temp_salary = temp_salary.replace('руб.', '')
                salary_max = int(temp_salary)
                currency = 'руб.'

        elif len(salary) == 5:
            temp_salary = salary[0].replace('\xa0', '')
            temp_salary = temp_salary.replace('руб.', '')
            salary_min = int(temp_salary)
            temp_salary = salary[1].replace('\xa0', '')
            temp_salary = temp_salary.replace('руб.', '')
            salary_max = int(temp_salary)
            currency = 'руб.'

        # print([salary_min, salary_max, currency])  # debug
        return [salary_min, salary_max, currency]

    def process_salary_hhru(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        # print(salary)  # debug
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
        # print([salary_min, salary_max, currency])  # debug
        return [salary_min, salary_max, currency]


