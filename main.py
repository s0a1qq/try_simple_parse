import requests
import csv
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def refined(s):
    return s.split(' ')[0].replace(',', '')

def write_csv(data):
    with open('plugins.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['url'], data['reviews']))

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    popular = soup.find_all('section')[1]
    plugins = popular.find_all('article')
    for plugin in plugins:
        name = plugin.find('h2').text
        url = plugin.find('h2').find('a').get('href')
        rating = refined(plugin.find('span', class_='rating-count').find('a').text)
        data = {
            'name': name,
            'url': url,
            'reviews': rating
        }
        write_csv(data)
    return len(plugins)

def main():
    url = 'https://wordpress.org/plugins'
    html = get_html(url)
    result = get_data(html)
    print(result)

if __name__ == '__main__':
    main()