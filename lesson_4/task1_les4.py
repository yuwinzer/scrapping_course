from pprint import pprint
from lxml import html
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get("https://lenta.ru/")
dom = html.fromstring(response.text)

items = dom.xpath("//time[@class='g-time']/../..")

all_news = []

for item in items:
    new = {}
    name = item.xpath(".//time[@class='g-time']/../../a/text()")
    name = ''.join(name)
    name = name.replace('\xa0', ' ')
    datetime = item.xpath(".//time[@class='g-time']/../../a/time/@datetime")
    datetime = ''.join(datetime)
    link = item.xpath(".//time[@class='g-time']/../../a/@href")
    link = ''.join(link)

    if (link[1:5]) == 'news':  # sometime here can be not a lenta.ru sourse, but moslenta.ru
        source = 'lenta.ru'
    else:
        source = (link.split('/'))[2]


    new['name'] = name
    new['link'] = link
    new['datetime'] = datetime
    new['source'] = source
    all_news.append(new)

pprint(all_news)


