import requests
import xmltodict
from datetime import date, timedelta
from bs4 import BeautifulSoup

list_of_times = []
primary_url = 'https://www.varzesh3.com/'
url = "https://www.varzesh3.com/sitemap/news"
result = requests.get(url)
data = xmltodict.parse(result.content)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2021, 9, 13)
end_date = date(2021, 9, 14)
for single_date in daterange(start_date, end_date):
    list_of_times.append(single_date.strftime("%Y-%m-%d"))
print(list_of_times)


def varzesh3_crawler():
    list_of_urls = []
    list_of_news = []
    for i in list_of_times:
        for j in range(len(data['urlset']['url'])):
            if i == data['urlset']['url'][j]['lastmod'][0:10]:
                list_of_urls.append(primary_url + data['urlset']['url'][j]['loc'][:14])

    for url in list_of_urls:
        raw_url = requests.get(url=url)
        content = BeautifulSoup(raw_url.text, 'html.parser')
        final_content = content.find('div', {'class': 'col-xs-12 news-page--news-text text-justify'})
        if final_content == None:
            continue
        else:
            list_of_news.append(final_content.text)
        for news in list_of_news:
            with open('news.txt', 'w+', encoding="utf8") as f:
                f.write(news)


def khabar_varzeshi_crawler():
    list_of_urls = []
    list_of_news = []
    for single_date in daterange(start_date, end_date):
        list_of_times.append(single_date.strftime("%Y-%m-%d"))

    for i in list_of_times:
        for j in range(len(data['urlset']['url'])):
            if i == data['urlset']['url'][j]['lastmod'][0:10]:
                list_of_urls.append(data['urlset']['url'][j]['loc'][:43])

    for url in list_of_urls:
        raw_url = requests.get(url=url)
        content = BeautifulSoup(raw_url.text, 'html.parser')
        a = content.find('a', {'itemdrop': 'headline'})
        b = content.find('div', {'class': 'item-text'})
        list_of_news.append(a)
        list_of_news.append(b)

    for news in list_of_news:
        with open('news.txt', 'w+', encoding="utf8") as f:
            f.write(news)


if url == "https://www.varzesh3.com/sitemap/news":
    print(varzesh3_crawler())
elif url == "https://www.khabarvarzeshi.com/sitemap/news/sitemap.xml":
    print(varzesh3_crawler())