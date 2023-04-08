import logging

import requests
from bs4 import BeautifulSoup

import db
from db import get_products
from services import helper
from services.helper import save_as_file

helper.prepare_logging()
logger = logging.getLogger('MAIN')

url = 'https://5ka.ru/rating/catalogue'
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

response = requests.get(url, headers=headers)
logger.info('request catalogue')
save_as_file(response.text, 'catalogue.html')
soup = BeautifulSoup(response.text, 'html.parser')

categories = soup.find_all('label', class_='radio-wrap')
id_by_category = {}
for category in categories[3:]:
    try:
        id_by_category[category.text.strip()] = category.next_element['value']
    except Exception as e:
        logger.warning(f'while parsing {category} : {e}')
logger.info('parsing id')

for category, id in id_by_category.items():
    logger.info(f'requesting info for {id}')
    data = get_products(id)
    save_as_file(str(data), f'category_{id}.json')
    try:
        modified_data = [(e['plu'], e['name'], e['promo']['date_begin'], e['promo']['date_end'], e['prices']['price_regular'], e['prices']['price_discount'], e['prices']['discount'], e['is_new'], category) for e in data['products']]
        db.insert_data(modified_data)
    except Exception as e:
        logger.warning(f'while parsing {category} : {e}')
