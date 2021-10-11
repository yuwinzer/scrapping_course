from pprint import pprint
from lxml import html
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get("https://lenta.ru/")
dom = html.fromstring(response.text)

# items = dom.xpath("//time[@class='g-time']/../..")
items = dom.xpath("//time[@class='g-time']/../..")

pprint(items)
all_news = []

for item in items:
    new = {}
    name = item.xpath(".//time[@class='g-time']/../../a/text()")
    datetime = item.xpath(".//time[@class='g-time']/../../a/time/@datetime")
    link = item.xpath(".//time[@class='g-time']/../../a/@href")
    # print(str(link)[3:7])
    if (str(link)[3:7]) == 'news':
        source = 'lenta.ru'
    else:
        source = (str(link).split('/'))[2]

    new['name'] = name
    new['link'] = link
    new['datetime'] = datetime
    new['source'] = source
    all_news.append(new)

pprint(all_news)


