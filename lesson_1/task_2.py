# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

#read API from a non committed file
with open('APIkeys.json', 'r') as API_keys_file:
    APIkeys = json.load(API_keys_file)
    API = APIkeys['exchangerate_api_1']

currency = 'USD'
url = f'https://v6.exchangerate-api.com/v6/{API}/latest/{currency}'

check_currencies = ['EUR', 'RUB', 'UAH']

response = requests.get(url)  # get a content from url
if response.ok:
    text = response.text  # get as a text
    data = json.loads(response.text)  # convert to json
#
    with open('1l_2t_data.json', 'w') as outfile:
        json.dump(data, outfile)

    print(f'Date: {data["time_last_update_utc"]} \n')
    print('Popular exchange rates:')
    for i in check_currencies:
        print(f"{i}: {data['conversion_rates'][i]}")
