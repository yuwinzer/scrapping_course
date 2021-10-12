from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

# create mongo database
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_collection = db.news_collection

news_collection.delete_many({})  # get empty before start

all_news = []

response = requests.get("https://lenta.ru/")
dom = html.fromstring(response.text)
items = dom.xpath("//time[@class='g-time']/../..")

for item in items:
    new = {}
    name = item.xpath(".//time[@class='g-time']/../../a/text()")
    name = ''.join(name)
    name = name.replace('\xa0', ' ')
    datetime = item.xpath(".//time[@class='g-time']/../../a/time/@datetime")
    datetime = ''.join(datetime)
    link = item.xpath(".//time[@class='g-time']/../../a/@href")
    link = ''.join(link)

    if (link[1:5]) == 'news':  # sometime here can be not a lenta.ru sourse, but external link to moslenta.ru
        source = 'lenta.ru'
        new['_id'] = link.split('/')[5]
    else:
        source = (link.split('/'))[2]
        # new['_id'] = need to catch this moslenta.ru case and get ID from link

    new['name'] = name
    new['link'] = link
    new['datetime'] = datetime
    new['source'] = source

    try:
        news_collection.insert_one(new)
    except dke:
        pass

    all_news.append(new)

pprint(all_news)


