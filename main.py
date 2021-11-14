import requests
from bs4 import BeautifulSoup
import csv

CSV = 'courses.csv'
HOST = 'https://www.coursera.org/courses?query=python'
URL = 'https://www.coursera.org/search?query=python&page='
HEADERS = {
    }


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_ ='lohp-rebrand')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='rc-SubFooterSection__content-column-link-text').get_text(),
                'author': item.find('span', class_='cds-1 partner-name css-mx49ok cds-3').get_text(),
                'numberOfreviews': item.find('span', class_='ratings-count').get_text(),
                'type': item.find('span', class_='cds-1 withoutGradient pillContainer css-v4ktz5 cds-3').get_text(),
                'level': item.find('span', class_='cds-1 difficulty css-lqm5si cds-3').get_text(),
                'numberOfPart': item.find('span', class_='enrollment-number').get_text()
            }
        )

    return cards


def save_doc(items, path):
    with open(path, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Course name', 'Author', 'Number of Reviews', 'Type', 'Level', 'Participate students'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['numberOfreviews'], item['type'], item['level'], item['numberOfPart']])


def parser():
    PAGENATION = input('How many pages do you want to parse: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(2, PAGENATION):
            print(f'Wait, parse the page number is: {page}')
            print(str(URL + str(page) + '&index=prod_all_launched_products_term_optimization'))
            html = get_html(URL + str(page) + '&index=prod_all_launched_products_term_optimization',params={})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print("Error")
parser()
