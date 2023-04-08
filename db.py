import json

import psycopg2
import requests
from psycopg2.extras import execute_values

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'location_id=13935; location=%7B%22id%22%3A13935%2C%22name%22%3A%22%D0%B3.%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D1%80-%D0%BD%20%D0%AE%D0%B6%D0%BD%D0%BE%D0%B5%20%D0%A2%D1%83%D1%88%D0%B8%D0%BD%D0%BE%22%2C%22type%22%3A%22city%22%2C%22new_loyalty_program%22%3Atrue%2C%22site_shops_count%22%3A0%2C%22region%22%3A%7B%22id%22%3A14%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%7D%2C%22isConfirmed%22%3Atrue%7D; TS01658276=01a93f7547124c99fe894eebb750edc3e36705b823778486c8e1ee62d40e4164b517c690912777032cd471f3f8088678836423f2bbf78f87d02be3d7620ed4da4b4f9175b3cb43f34da74c5f2cf3bda0107963ad51; TS010a09ac=01a93f75475de06d0532b39d03983c2d02b79d53c14dc6b115fb63d1fdd6e6f1be34bfaab0fc21b4880f610950ae10ef9e4c9078deaa601f5c9db2402070b3496ad592fcbb',
    'Host': '5ka.ru',
    'Referer': 'https://5ka.ru/rating/catalogue',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-User-Store': '31Z6',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS"}


def connectPg():
    conn = psycopg2.connect(host='localhost', port='5432', dbname='postgres', password="12345")
    curs = conn.cursor()
    return conn, curs


def disconnectPg(conn, curs):
    curs.close()
    conn.close()


def insert_data(data):
    conn, curs = connectPg()
    execute_values(curs, 'insert into products (plu, name, date_begin, date_end, price_regular, price_discount, discount, is_new, category) VALUES %s;', data)
    conn.commit()
    disconnectPg(conn, curs)


def get_products(id):
    responce = requests.get(url=f"https://5ka.ru/api/v1/products/?limit=0&offset=0&rates_count_from=30&is_promo=false&category={id}&rating_order=", headers=HEADERS)
    return responce.json()


if __name__ == '__main__':
    with open('data/test.json', 'r') as file:
        data = json.load(file)
    modified_data = [(e['plu'], e['name'], e['promo']['date_begin'], e['promo']['date_end'], e['prices']['price_regular'], e['prices']['price_discount'], e['prices']['discount'], e['is_new']) for e in data['products']]
    print(modified_data)
    insert_data(modified_data)
