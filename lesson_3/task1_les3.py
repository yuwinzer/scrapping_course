from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import requests
import json
from bs4 import BeautifulSoup as bs

# create mongo database vacancies with ukr_headhunter collection
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
ukr_headhunter = db.ukr_headhunter     # persons - коллекция, ви - база данных

# ukr_headhunter.delete_many({})  # очистка перед наполнением

url = 'https://grc.ua/search/vacancy'
params = {'text': 'Django',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

vacancies = []
while True:
    response = requests.get(url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    if not vacancy_list or not response.ok:
        break

    for vacancy_div in vacancy_list:
        vacancy_data = {}
        vacancy_header = vacancy_div.find('a')
        vacancy_name = vacancy_header.text
        vacancy_link = vacancy_header.get('href')

        vacancy_salary_info = vacancy_div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary_info:

            vacancy_salary_raw = vacancy_salary_info.text
            vacancy_salary_raw = vacancy_salary_raw.replace('\u202f', '')
            vacancy_salary_raw = vacancy_salary_raw.split(' ')
            # print(vacancy_salary_raw)
            # print(len(vacancy_salary_raw))

            if len(vacancy_salary_raw) == 3:
                if vacancy_salary_raw[0] == 'от':
                    vacancy_data['salary_min'] = int(vacancy_salary_raw[1])
                    vacancy_data['salary_max'] = None
                    vacancy_data['salary_currency'] = vacancy_salary_raw[2]
                elif vacancy_salary_raw[0] == 'до':
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = int(vacancy_salary_raw[1])
                    vacancy_data['salary_currency'] = vacancy_salary_raw[2]
            elif len(vacancy_salary_raw) == 4:
                vacancy_data['salary_min'] = int(vacancy_salary_raw[0])
                vacancy_data['salary_max'] = int(vacancy_salary_raw[2])
                vacancy_data['salary_currency'] = vacancy_salary_raw[3]

        else:
            vacancy_data['salary_min'] = None
            vacancy_data['salary_max'] = None
            vacancy_data['salary_currency'] = None

        vacancy_data['_id'] = int(vacancy_link[28:36])
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['website'] = 'grc.ua'

        vacancies.append(vacancy_data)

        try:
            ukr_headhunter.insert_one(vacancy_data)
        except dke:
            pass
    params['page'] += 1

# pprint(vacancies)

# with open('task1_les3.json', 'w') as outfile:
#     json.dump(vacancies, outfile, ensure_ascii=False) # с json есть ошибки, надо разобраться почему

for doc in ukr_headhunter.find({}):
    pprint(doc)

pprint(len(vacancies))  # 560 vacancies at latest check