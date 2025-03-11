import requests
from bs4 import BeautifulSoup


access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NDA5MDgxOTgsImV4cCI6MTc0MDkxMTc5OCwiY3VzdG9tZXIiOiIzNTI5NiIsImlkIjoiZmUwODllOTktYmI2My00YmYyLThiNjEtNDAyZTZkNzQyM2M4IiwibG9naW4iOiJjdmV0b290In0.lu88onj09H5hRJteBlupCBuKW3jX4uIE6kLkcTkOrgaJUwVufgE38jw8nGaHzKmeXhbnmZogsZ-rFQpLSJPu11IHzyriiIhAMawLNCUGNYQdIRZEn36OMQHqZnch1m0XLiwurX923GlaRQVhoW6zWXIWpMaNI7dceY7Y2yV6m8W311otJBElZD0PKLH0Grj2_KZkRyWJknEojOQ9_QlA9NdeEzBA0eGLyKJty_V9eYpaXs3TidaOYC9-vQ1GBK9XP6UB9PRmIkFG4fG94O4ySUL4EWz0uiDo56Q_cRg9YD7wCngwD6fYjYN0zgJlxtNxVWg1L0cC4SgSrDgd4Bb7Kg"  # Замените на реальный токен

url = 'https://cvetoot.posiflora.com/admin/orders'

session = requests.Session()

# Получаем страницу с заказами
response = session.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)

# Здесь нужно найти элемент, который содержит количество завершенных заказов
# Например, если это div с классом 'completed-orders':
# completed_orders = soup.find('div', class_='ps-tab__badge ps-badge ps-badge_order_done')

# print(f'Количество завершенных заказов: {completed_orders}')