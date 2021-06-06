import pickle
import json 
from bs4 import BeautifulSoup
import re
import time

f = open('data.bin', 'rb')
laptops = pickle.load(f)


new_laptop = []

for ln in laptops:
    sku = []
    image = []
    characteristics = []

    if ln['site'] == 'onlinetrade':
        soup = BeautifulSoup(ln['charapt'], 'lxml')
        chrs = soup.find_all('li', {'class' : 'featureList__item'})
        for chr in chrs:
            characteristics.append(chr.text)
        urls = re.findall(r'http(?:s)?://\S+', ln['charapt'])
        for url in urls:
            url = url.replace('\'', '').replace(',', '').replace(']', '').replace('[', '')
            image.append({'url' : url})

    if ln['site'] == 'novomarket':  
        soup = BeautifulSoup(ln['charapt'], 'lxml')
        names = soup.find_all('dl', {'class' : 'expand-content clearfix'})

        for name in names: 
            divs = name.find_all('div')
            for div in divs:
                label = div.find('dt').text
                value = div.find('dd').text
                characteristics.append(f'{label}:{value}')

        urls = re.findall(r'http(?:s)?://\S+', ln['charapt'])
        for url in urls:
            url = url.replace('\'', '').replace(',', '').replace(']', '').replace('[', '')
            image.append({'url' : url})

    if ln['site'] == 'regard': # Очень не приятный
        soup = BeautifulSoup(str(ln['charapt']), 'lxml')
        names = soup.find_all('tr')
        for name in names: 
            n = 0
            label = None
            mean = None
            values = name.find_all('td')
            for value in values:
                if value.text == 'Основные': # Не работает с or почему то :(
                    continue
                if value.text == 'Дисплей':
                    continue
                if value.text == 'Процессор':
                    continue
                if value.text == 'Оперативная память':
                    continue
                if value.text == 'Жесткий диск':
                    continue
                if value.text == 'Видео':
                    continue
                if value.text == 'Аудио':
                    continue
                if value.text == 'Привод':
                    continue
                if value.text == 'Сеть':
                    continue
                if value.text == 'Дополнительно':
                    continue
                n+=1
                if n == 1:
                    label = value.text
                    label = str(label).replace(' \xa0', '')
                if n % 2 == 0:
                    mean = value.text
                    characteristics.append(f'{label}:{mean}')
                    n = 0
        urls = re.findall(r'http(?:s)?://\S+', str(ln['charapt']))
        
        for url in urls:
            url = url.replace('\'', '').replace(',', '').replace(']', '').replace('[', '')
            image.append({'url' : url})

    new_laptop.append({'sku' : ln['article'], "image" : image, "characteristics" : characteristics})
print('start')
new_charapt = []
for char in new_laptop:
    for i in char['characteristics']:
        new_charapt.append(({'vid_name' : 'one_of', 'char_name' : i.split(':')[0], 'value' : i.split(':')[1]}))
    char['characteristics'] = new_charapt
    new_charapt = []


      


f = open('test1.json', 'w', encoding='utf8')
json.dump(new_laptop,f, indent=3,ensure_ascii=False)