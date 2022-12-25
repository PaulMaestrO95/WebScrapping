import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


new_list = []


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


def get_array():
    for link in get_urls():
        response = requests.get(link, headers=get_headers())
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_='main-content')
        pattern = r'.*((D|d)jango).*((F|f)lask).*'
        adress = {'data-qa': 'vacancy-view-raw-address'}
        try:
            city = data.find(attrs=adress).text
        except AttributeError:
            city = 'Город не указан'

        if re.search(pattern, (data.text)):
            new_list.append({
                'url': link,
                'salary': data.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text.replace('\xa0', ''),
                'name': data.find('h1').text,
                'city': city
            })
        else:
            continue
        pprint(new_list)

def get_json():
    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(new_list, v, ensure_ascii=False)


