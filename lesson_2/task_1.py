# 1. Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать
# несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать
# в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
# dataFrame через pandas. Сохраните в json либо csv.

import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint


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
                    vacancy_data['salary_min'] = vacancy_salary_raw[1]
                    vacancy_data['salary_max'] = None
                    vacancy_data['salary_currency'] = vacancy_salary_raw[2]
                elif vacancy_salary_raw[0] == 'до':
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = vacancy_salary_raw[1]
                    vacancy_data['salary_currency'] = vacancy_salary_raw[2]
            elif len(vacancy_salary_raw) == 4:
                vacancy_data['salary_min'] = vacancy_salary_raw[0]
                vacancy_data['salary_max'] = vacancy_salary_raw[2]
                vacancy_data['salary_currency'] = vacancy_salary_raw[3]

        else:
            vacancy_data['salary_min'] = None
            vacancy_data['salary_max'] = None
            vacancy_data['salary_currency'] = None

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['website'] = 'grc.ua'

        vacancies.append(vacancy_data)
    params['page'] += 1

pprint(vacancies)
pprint(len(vacancies))  # 560 vacancies at latest check

with open('2l_1t_data.json', 'w') as outfile:
    json.dump(vacancies, outfile, ensure_ascii=False)


