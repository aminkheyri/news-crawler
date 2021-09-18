import requests
import xmltodict
from datetime import date, timedelta

list_of_times = []
list_of_news = []
url = "https://www.khabarvarzeshi.com/sitemap/news/sitemap.xml"
result = requests.get(url)
data = xmltodict.parse(result.content)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2021, 9, 16)
end_date = date(2021, 9, 20)
for single_date in daterange(start_date, end_date):
    list_of_times.append(single_date.strftime("%Y-%m-%d"))

for i in list_of_times:
    for j in range(len(data['urlset']['url'])):
        if i == data['urlset']['url'][j]['lastmod'][0:10]:
            list_of_news.append(data['urlset']['url'][j]['loc'][43:])

print(dict(enumerate(list_of_news, 1)))
