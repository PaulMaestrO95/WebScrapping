from pprint import pprint
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re

new_dict = []

def get_headers():
    headers = Headers(browser='random_browser', os='random_os').generate()
    return headers


def get_urls():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    response = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(response.text, features='lxml')
    data = soup.find_all('a', class_="serp-item__title")
    for l in data:
        link = l['href']
        yield link


def array():
    for link in get_urls():
        try:
            response = requests.get(link, headers=get_headers())
            soup = BeautifulSoup(response.text, 'lxml')
            data = soup.find('div', class_='main-content')
            researh = r'.*((D|d)jango).*((F|f)lask).*'
            if re.match(researh, data.find('div',class_='vacancy-title').text):
                new_dict.append({
                    'url':link,
                    'salary':data.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text,
                    'name':data.find('div',class_='vacancy-title').text,
                    'city':data.find('div', class_='vacancy-section').text
                })
            pprint(new_dict)
        except AttributeError:
            continue



array()
