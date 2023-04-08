import requests
from bs4 import BeautifulSoup

from services.helper import save_as_file

url = 'https://5ka.ru/rating/catalogue'
headers = {
"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
'Accept': 'application/json, text/plain, */*'
}

response = requests.get(url, headers=headers)
save_as_file(response.text, 'catalogue.html')
soup = BeautifulSoup(response.text, 'html.parser')


