import requests
import json
import time

# Функция для авторизации и получения токена
def get_access_token():
    url = 'https://cvetoot.posiflora.com/api/v1/sessions'
    payload = {
        "data": {
            "type": "sessions",
            "attributes": {
                "username": "cvetoot",
                "password": "wowtDCx7"
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['data']['attributes']['accessToken']
    else:
        print(f"Ошибка при получении токена: {response.status_code}")
        return None

# Функция для получения количества завершенных заказов
def get_done_orders_count(headers):
    url = "https://cvetoot.posiflora.com/api/v1/orders?page%5Bnumber%5D=1&page%5Bsize%5D=1&filter%5Bstatuses%5D=done"
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Ошибка авторизации
        return None
    data = response.json()
    return data['meta']['total']

# Функция для получения данных о заказе по его номеру страницы
def get_order_data(page_number, headers):
    url = f"https://cvetoot.posiflora.com/api/v1/orders?page%5Bnumber%5D={page_number}&page%5Bsize%5D=1&filter%5Bstatuses%5D=done&include=source%2Cstore%2Cstore.timezone%2Ccustomer%2CpostedBy%2CcreatedBy%2ClockedBy%2Cpayments%2Cpayments.method%2Cdiscounts%2Ccourier%2Cflorist&sort=createdAt"
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Ошибка авторизации
        return None
    return response.json()

# Функция для извлечения данных из JSON-а
def extract_data(data):
    result = {}

    # Поиск данных о клиенте в included
    customer_data = None
    for item in data['included']:
        if item['type'] == 'customers':
            customer_data = item['attributes']
            break

    # Если данные о клиенте найдены
    if customer_data:
        result['name'] = customer_data['title']
        result['phone'] = customer_data['phone']
    else:
        result['name'] = "Не указано"
        result['phone'] = "Не указано"

    # Данные о заказе
    order_data = data['data'][0]['attributes']  # Данные о заказе
    result['budget'] = order_data['totalAmount']
    result['purchase_date'] = order_data['date']
    result['docNo'] = order_data['docNo']

    return result

# Функция для сохранения результатов в файл
def save_results(results, filename='results.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Результаты сохранены в файл {filename}")

# Основная логика программы
def main():
    # Получаем токен при старте
    access_token = get_access_token()
    if not access_token:
        print("Не удалось получить токен. Завершение работы.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Список для хранения результатов
    results = []

    # Сначала собираем все существующие завершенные заказы
    print("Сбор существующих завершенных заказов...")
    done_orders_count = get_done_orders_count(headers)
    if done_orders_count is None:  # Ошибка авторизации
        access_token = get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"
        done_orders_count = get_done_orders_count(headers)

    for i in range(1, done_orders_count + 1):
        order_data = get_order_data(i, headers)
        if order_data is None:  # Ошибка авторизации
            access_token = get_access_token()
            headers["Authorization"] = f"Bearer {access_token}"
            order_data = get_order_data(i, headers)
        result = extract_data(order_data)
        results.append(result)
        print(f"Обработан заказ {i} из {done_orders_count}")

    # Сохраняем старые заказы
    save_results(results)

    # Бесконечный цикл для проверки новых заказов
    print("Ожидание новых заказов...")
    last_done_orders_count = done_orders_count

    while True:
        # Проверяем количество завершенных заказов
        current_done_orders_count = get_done_orders_count(headers)
        if current_done_orders_count is None:  # Ошибка авторизации
            access_token = get_access_token()
            headers["Authorization"] = f"Bearer {access_token}"
            current_done_orders_count = get_done_orders_count(headers)

        # Если количество завершенных заказов увеличилось
        if current_done_orders_count > last_done_orders_count:
            print(f"Найдены новые заказы. Текущее количество: {current_done_orders_count}")

            # Собираем данные о новых заказах
            for i in range(last_done_orders_count + 1, current_done_orders_count + 1):
                order_data = get_order_data(i, headers)
                if order_data is None:  # Ошибка авторизации
                    access_token = get_access_token()
                    headers["Authorization"] = f"Bearer {access_token}"
                    order_data = get_order_data(i, headers)
                result = extract_data(order_data)
                results.append(result)
                print(f"Обработан новый заказ {i}")

            # Обновляем количество завершенных заказов
            last_done_orders_count = current_done_orders_count

            # Сохраняем обновленные результаты
            save_results(results)

        # Пауза перед следующей проверкой (например, 60 секунд)
        time.sleep(60)

# Запуск программы
if __name__ == "__main__":
    main()