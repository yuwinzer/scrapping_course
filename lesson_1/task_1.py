# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

# repos link for test user Octocat
url = 'https://api.github.com/users/octocat/repos'

response = requests.get(url)  # get a content from url
if response.ok:
    text = response.text  # get as a text
    reposContent = json.loads(response.text)  # convert to json

    with open('1l_1t_data.json', 'w') as outfile:
        json.dump(reposContent, outfile)

    # list of repos names
    print('Repos names:')
    for i in reposContent:
        print(i['name'])


