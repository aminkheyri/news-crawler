import requests
import xmltodict
import datetime
from bs4 import BeautifulSoup


dict_of_news = {}
list_of_news = []
list_of_requested_times = []
primary_url = 'https://www.varzesh3.com/'
url = "https://www.varzesh3.com/sitemap/news"
result = requests.get(url)
data = xmltodict.parse(result.content)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


start_date = datetime.date(2021, 9, 21)
end_date = datetime.date(2021, 9, 22)
for single_date in daterange(start_date, end_date):
    list_of_requested_times.append(single_date.strftime("%Y-%m-%d"))


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
    return content.text


def get_varzesh3_information():
    for i in list_of_requested_times:
        for j in range(len(data['urlset']['url'])):
            if i == data['urlset']['url'][j]['lastmod'][0:10]:
                dict_of_news['url'] = primary_url + data['urlset']['url'][j]['loc'][:14]
                dict_of_news['title'] = data['urlset']['url'][j]['loc'][14:]
                dict_of_news['lastmod'] = datetime.datetime.strptime(
                    data['urlset']['url'][j]['lastmod'], '%y-%m-%d')
                dict_of_news['content'] = get_content_of_varzesh3_url(primary_url + data['urlset']['url'][j]['loc'][:14])
                list_of_news.append(dict_of_news.copy())

    return list_of_news


def get_khabarvarzeshi_information():
    for i in list_of_requested_times:
        for j in range(len(data['urlset']['url'])):
            if i == data['urlset']['url'][j]['lastmod'][0:10]:
                dict_of_news['url'] = data['urlset']['url'][j]['loc'][:43]
                dict_of_news['title'] = data['urlset']['url'][j]['loc'][43:]
                dict_of_news['lastmod'] = datetime.datetime.strptime(data['urlset']['url'][j]['lastmod'],
                                                                     '%y-%m-%d')
                dict_of_news['content'] = get_content_of_khabarvarzeshi_url(data['urlset']['url'][j]['loc'][:43])
                list_of_news.append(dict_of_news.copy())
    return list_of_news


if url == "https://www.varzesh3.com/sitemap/news":
    print(get_varzesh3_information())
elif url == "https://www.khabarvarzeshi.com/sitemap/news/sitemap.xml":
    print(get_khabarvarzeshi_information())
