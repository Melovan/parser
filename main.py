import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-item-footer-cols')
    for i in items:
        price = i.find('span', class_='catalog-item-price text-h5').get_text()
        price = price.replace(' ', '').replace('Р', '')
        name = i.find('a', class_='catalog-item-link').find('span').get_text()
        print(price)
        if name is None:
            continue
        catalog.append({
            'name': name,
            'price': price,
        })
    return catalog


def append_file(items, path):
    with open(path, 'a+', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for item in items:
            writer.writerow([item['name'], item['price']])


def parse():
    filename = 'watches.csv'
    with open(filename, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Названия товара', 'Цена товара (в рублях)'])
    for URL in ['https://www.alltime.ru/watch/?PAGEN_1='+str(i) for i in range(1, 5)]:
        html = get_html(URL)
        if html.status_code == 200:
            html = get_content(html.text)
        else:
            print('Error')
        append_file(html, filename)


parse()
