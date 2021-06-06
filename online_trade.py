import requests 
from bs4 import BeautifulSoup
from termcolor import colored
import Pythontojson

global headers, domain, findline, laptops
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 YaBrowser/20.8.2.92 Yowser/2.5 Safari/537.36'}
domain = 'https://www.onlinetrade.ru'
findline = 'https://www.onlinetrade.ru/sitesearch.html?query='



def getlink_onlinetrade (part):
    url = findline + part
    link = None # Не известно, но последний if сослался на не существ. переменную 332
    try:
        page = requests.get(url, headers=headers, timeout=10)
    except:
        print(colored("Connection error", 'red'))
        return None

    soup = BeautifulSoup(page.text, 'lxml')
    soup = soup.find_all('div', {'class' : 'indexGoods__item'}) # Могут упасть несколько значений из за не жесткой сортировки поиска
    if len(soup) > 1:
        for cage in soup:
            title = cage.find('span', {'class' : 'indexGoods__item__fastView js__ajaxExchange ic__set ic__set__viewed'}).get('title', 'No title attribute')
            try: # был какой то собачий корм
                if title[title.rindex('(') + 1 : title.rindex(')')] == part:
                    link = domain + cage.find('a').get('href')
                    
                else:
                    continue
            except:
                link = None
    elif len(soup) == 0:
        link = None
    else:
        link = domain + soup[0].find('a').get('href')

    if link:
        print(colored("Added", 'green'), part)
    else:
        print(colored("Not found -", 'yellow'), part)

    return link


def get_charapt_onlinetrade(link):
    charapt = []
    url = link
    try:
        page = requests.get(url, headers=headers, timeout=10)
    except:
        print(colored("Connection on charpt error!!!", 'red'))
        return None
    soup = BeautifulSoup(page.text, 'lxml')
    chr = soup.find_all('li', {'class' : 'featureList__item'})
    for i in chr:
        charapt.append(i)
    img = soup.find_all('div', {'class' : 'swiper-slide'})
    for i in img:
        charapt.append(i.find('a').get('href'))
        
    return charapt