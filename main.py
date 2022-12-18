from bs4 import BeautifulSoup
from pprint import pprint
import requests
from fake_headers import Headers
import json
import re

def get_headers():
     headers = Headers(browser='random_browser', os='random_os').generate()
     return headers

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
html = requests.get(url, headers=get_headers()).text
soup = BeautifulSoup(html, features='lxml')
data = soup.find_all('a', class_="serp-item__title")
links = []
for l in data:
    link = l['href']
    links.append(link)


pprint(links)











