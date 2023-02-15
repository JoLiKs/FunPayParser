import sys
import requests
from bs4 import BeautifulSoup
from data import Lot
import re
import db_client


PARSER_NAME = 'funpay'


def get_lots(min_price, max_price, count_lots):
    lots_arr = []
    resp = requests.get(f'https://funpay.com/lots/436/')
    html = BeautifulSoup(resp.content, 'html.parser')
    if count_lots > len(html.find_all("a")):
        print(f'Запрашиваемое количество лотов ({count_lots}) больше, чем общее число лотов ({len(html.find_all("a"))})')
        sys.exit()
    counter = 0
    for a in html.find_all('a', href=True, class_='tc-item lazyload-hidden'):
        if counter == count_lots: break;
        title = a.find('div', class_='tc-desc-text').text.strip()
        price = float(re.sub('[^0-9.]', '', a.find('div', class_='tc-price').text.strip()))
        if price > min_price and price < max_price:
            rp = a.find('div', class_='rating-stars')
            if rp is not None: seller_rep = int(re.sub('[^0-9]', '', rp['class'][1]))
            else: seller_rep = 0
            lots_arr.append(Lot(
                link=a['href'],
                reference=PARSER_NAME,
                price=price,
                title=title,
                seller_rep=seller_rep,
                ))
            counter +=1
            print(f'Спаршено {counter} из {count_lots}')
            ready_lots = list(lots_arr)
    if len(lots_arr) == 0:
        print("По заданной цене ничего не найдено")
        sys.exit()
    if len(lots_arr) < count_lots:
        print(f"По заданной цене найдено только {len(lots_arr)} предложений")
    return ready_lots


def save_lots(lots):
    db_client.create_lots_table()
    counter = 1;
    for lot in lots:
        print(f'Загружено в базу {counter} из {len(lots)}')
        db_client.insert_lot(lot)
        counter+=1


def get_last_lots():
    min_price = int(input("Введите минимальную цену\n"))
    max_price = int(input("Введите максимальную цену\n"))
    count_lots = int(input("Введите желаемое число предложений\n"))
    lots = get_lots(min_price, max_price, count_lots)
    save_lots(lots)


get_last_lots()

