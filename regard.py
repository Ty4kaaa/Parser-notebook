import os
import requests 
from bs4 import BeautifulSoup
from termcolor import colored
import openpyxl
import pickle
from online_trade import get_charapt_onlinetrade, getlink_onlinetrade
from novomarket import get_charapt_novomarket, get_link_novomarket

global headers, domain, findline, laptops
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 YaBrowser/20.8.2.92 Yowser/2.5 Safari/537.36'}
domain = 'https://www.regard.ru'
findline = 'https://www.regard.ru/catalog/?query='




def get_link_regard(part):
    url = findline + part
    link = None # Не известно, но последний if сослался на не существ. переменную 332
    try:
        page = requests.get(url, headers=headers, timeout=4)
    except:
        print(colored("Connection error", 'red'))
        return None
    soup = BeautifulSoup(page.text, 'lxml')
    soup = soup.find_all('div', {'class' : 'block'})
    for block in soup:
        if part in block.find('a').find('img').get('alt'):
            link = domain + block.find('div', {'class' : 'aheader'}).find('a').get('href')
            print(colored("Added", 'green'), part)
            return link
    print(colored("Not found -", 'yellow'), part)


def get_charapt_regard(link):
    charapt = []
    url = link
    try:
        page = requests.get(url, headers=headers, timeout=10)
    except:
        print(colored("Connection on charpt error!!!", 'red'))
        return None
    soup = BeautifulSoup(page.text, 'lxml')
   

    chr = soup.find('div', {"id" : "tabs-1"})

    for i in chr:
        charapt.append(i)

    img = soup.find_all('img', {'class' : 'big_preview'})

    for i in img:
        charapt.append(domain + i.get('src', 'No src attribute'))
        
    return charapt