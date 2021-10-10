from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['vacancies']
ukr_headhunter = db.ukr_headhunter

# result = ukr_headhunter.find({})
# pprint(list(result[0]))

for doc in ukr_headhunter.find({'salary_min': {'$gt': 5000}}):
    pprint(doc)

# поиск зарплаты по 3 полям с учетом валюты
vac_count = 0
for doc in ukr_headhunter.find({
            '$and': [
                {
                    '$or': [
                        {'salary_min': {'$gt': 5000}},
                        {'salary_max': {'$gt': 5000}}
                    ]
                },
                {
                    "salary_currency": "USD"
                }
            ]
        }):
    vac_count += 1
    pprint(doc)
print(f'Найдено {vac_count} вакансий')
