import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


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
        response = requests.get(link, headers=get_headers())
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_='main-content')
        url = link
        adress = {'data-qa': 'vacancy-view-raw-address'}
        salary = data.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text
        name = data.find('h1').text
        try:
            city = data.find(attrs=adress).text
        except AttributeError:
            city = 'Город не указан'
        print(url, salary, name, city)
        # yield url, salary, name, city


array()

# pattern = r'.*((D|d)jango).*((F|f)lask).*'
# if re.search(pattern, (data.find('div', class_='vacancy-description').text)):
#     try:
#         new_list.append({'url':link, 'salary': salary, 'name': name, 'city': city})
#     except:
#         new_list.append('вакансия в архиве')