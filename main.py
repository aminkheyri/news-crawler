import requests
import xmltodict
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup


dict_of_news = {}
list_of_news = []
primary_url = 'https://www.varzesh3.com/'
url = "https://www.varzesh3.com/sitemap/news"
result = requests.get(url)
data = xmltodict.parse(result.content)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2021, 10, 20)
end_date = date(2021, 10, 25)


def get_content_of_varzesh3_url(given_url):
    raw_url = requests.get(url=given_url)
    content = BeautifulSoup(raw_url.text, 'html.parser')
    final_content = content.find('div', {'class': 'col-xs-12 news-page--news-text text-justify'})
    if final_content == None:
        pass
    else:
        return final_content.text


def get_content_of_khabarvarzeshi_url(given_url):
    raw_url = requests.get(url=given_url)
    content = BeautifulSoup(raw_url.text, 'html.parser')
    content = content.find('div', {'class': 'item-text'})
    if content == None:
        pass
    else:
        return content.text


def get_varzesh3_information():
    for single_date in daterange(start_date, end_date):
        single_date = single_date.strftime("%Y-%m-%d")
        for j in range(len(data['urlset']['url'])):
            if single_date == data['urlset']['url'][j]['lastmod'][0:10]:
                dict_of_news['url'] = primary_url + data['urlset']['url'][j]['loc'][:14]
                dict_of_news['title'] = data['urlset']['url'][j]['loc'][14:]
                dict_of_news['lastmod'] = datetime.strptime(
                    data['urlset']['url'][j]['lastmod'][0:10], '%Y-%m-%d')
                dict_of_news['content'] = get_content_of_varzesh3_url(primary_url + data['urlset']['url'][j]['loc'][:14])
                list_of_news.append(dict_of_news.copy())

    return list_of_news


def get_khabarvarzeshi_information():
    for single_date in daterange(start_date, end_date):
        single_date = single_date.strftime("%Y-%m-%d")
        for j in range(len(data['urlset']['url'])):
            if single_date == data['urlset']['url'][j]['lastmod'][0:10]:
                dict_of_news['url'] = data['urlset']['url'][j]['loc'][:43]
                dict_of_news['title'] = data['urlset']['url'][j]['loc'][43:]
                dict_of_news['lastmod'] = datetime.strptime(data['urlset']['url'][j]['lastmod'][0:10],
                                                                     '%Y-%m-%d')
                dict_of_news['content'] = get_content_of_khabarvarzeshi_url(data['urlset']['url'][j]['loc'][:43])
                list_of_news.append(dict_of_news.copy())
    return list_of_news

