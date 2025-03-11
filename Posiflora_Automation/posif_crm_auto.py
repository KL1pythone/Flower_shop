import requests
import json
import time

# Конфигурация AmoCRM
AMOCRM_SUBDOMAIN = 'cvetoot'
AMOCRM_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjM5NDllYzBjZmYzM2JhYjE3MDQ4NGQxYTRjYWM3YmMwNWQwZGU1NWFmY2E1MmYwMjIxZTZlYTNkNzlmODRjNTBlZGMzNzIwNTVmMDk0MGYyIn0.eyJhdWQiOiI3YWNiYzgwNS1kNTIxLTQ4ZmEtODgzYS1kYTkzOWIxN2ZmN2MiLCJqdGkiOiIzOTQ5ZWMwY2ZmMzNiYWIxNzA0ODRkMWE0Y2FjN2JjMDVkMGRlNTVhZmNhNTJmMDIyMWU2ZWEzZDc5Zjg0YzUwZWRjMzcyMDU1ZjA5NDBmMiIsImlhdCI6MTc0MTAwODcyMCwibmJmIjoxNzQxMDA4NzIwLCJleHAiOjE4NjcxOTA0MDAsInN1YiI6Ijg1MDM0MTQiLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzAzNjU2NzcsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbImNybSIsImZpbGVzIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyIsInB1c2hfbm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiI0NWFlNDhkZS0xY2RjLTQzMDktYTNjOS1mY2E5NmNjNGFjODgiLCJhcGlfZG9tYWluIjoiYXBpLWIuYW1vY3JtLnJ1In0.RJJXQuLJzL7FT-U16FiOdhE-FsLJ2GCv6QxU8YaeuVaLjAr4wXkBeejgN4HgPXubN3PMVcN7D4U83po4lldLmi6_v6sj_2UnvYSOmmE8JJC6vF7oqXYq1q__la2E2v2ImVTlhfWW-shppE-J0CN3lGJlj0HFRNEPeYCJy1Oyb_Zs7IaVhaaCSBdDzGafPUhIdYiofDramgnBgribgIAmPZJEWyzCFxX58dCoNFH5dWn5oVDwM-UhIBjpt4Zx1UAuU7orQxZ15cZloSKKwfvA7lYLOsjfbXcdpdbIABjlji9z-QR1CY7EAqk5sb1z0lZmUfWlzWyvk6FPYgcFhq072w'
AMOCRM_BASE_URL = f'https://{AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4'

# Конфигурация Posiflora
POSIFLORA_API_URL = 'https://cvetoot.posiflora.com/api/v1'
POSIFLORA_CREDENTIALS = {
    "username": "cvetoot",
    "password": "wowtDCx7"
}

# Настройка заголовков
amocrm_headers = {
    'Authorization': f'Bearer {AMOCRM_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def create_contact(name, phone, bonus_points):
    """Создание контакта в AmoCRM с бонусами"""
    print(f"Создание контакта для {name}")
    contact_data = {
        "name": name,
        "custom_fields_values": [
            {
                "field_id": 568643,
                "values": [{"value": phone, "enum_id": 381257}]
            },
            {
                "field_id": 1421111,
                "values": [{"value": str(bonus_points) if bonus_points else '0'}]
            }
        ]
    }

    try:
        response = requests.post(
            f'{AMOCRM_BASE_URL}/contacts',
            headers=amocrm_headers,
            json=[contact_data]
        )
        response.raise_for_status()
        return response.json()['_embedded']['contacts'][0]['id']
    except Exception as e:
        print(f"Ошибка создания контакта: {str(e)}")
        return None

def create_lead(name, budget, contact_id, purchase_date):
    """Создание сделки в AmoCRM"""
    print(f"Создание сделки для контакта {contact_id}")
    custom_fields = [
        {
            "field_id": 1387641,
            "values": [{"value": purchase_date}]
        }
    ]

    lead_data = {
        "name": name,
        "price": budget,
        "_embedded": {
            "contacts": [{"id": contact_id, "is_main": True}]
        },
        "custom_fields_values": custom_fields
    }

    try:
        response = requests.post(
            f'{AMOCRM_BASE_URL}/leads',
            headers=amocrm_headers,
            json=[lead_data]
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Ошибка создания сделки: {str(e)}")
        return False

def get_posiflora_token():
    """Авторизация в Posiflora"""
    print("Авторизация в Posiflora...")
    try:
        response = requests.post(
            f'{POSIFLORA_API_URL}/sessions',
            json={"data": {"type": "sessions", "attributes": POSIFLORA_CREDENTIALS}}
        )
        return response.json()['data']['attributes']['accessToken']
    except Exception as e:
        print(f"Ошибка авторизации: {str(e)}")
        return None

def get_customer_bonus(customer_id, headers):
    """Получение бонусных баллов"""
    if not customer_id:
        return None
    try:
        response = requests.get(
            f'{POSIFLORA_API_URL}/customers/{customer_id}',
            headers=headers
        )
        return response.json()['data']['attributes'].get('currentPoints')
    except Exception as e:
        print(f"Ошибка получения бонусов: {str(e)}")
        return None

def get_done_orders_count(headers):
    """Получение количества завершенных заказов с обработкой ошибок"""
    url = "https://cvetoot.posiflora.com/api/v1/orders?page[number]=1&page[size]=1&filter[statuses]=done"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        
        # Проверка наличия ключа 'meta'
        if 'meta' not in data:
            print("❌ В ответе отсутствует ключ 'meta'")
            return None
        
        return data['meta']['total']
    except requests.exceptions.RequestException as e:
        print(f"🚨 Ошибка запроса: {str(e)}")
        return None
    except KeyError as e:
        print(f"🔑 Ошибка ключа в JSON: {str(e)}")
        return None
    except Exception as e:
        print(f"⚠️ Неожиданная ошибка: {str(e)}")
        return None

def get_order_data(page_number, headers):
    """Получение данных заказа"""
    url = f"https://cvetoot.posiflora.com/api/v1/orders?page%5Bnumber%5D={page_number}&page%5Bsize%5D=1&filter%5Bstatuses%5D=done&include=source%2Cstore%2Cstore.timezone%2Ccustomer%2CpostedBy%2CcreatedBy%2ClockedBy%2Cpayments%2Cpayments.method%2Cdiscounts%2Ccourier%2Cflorist&sort=createdAt"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Ошибка получения заказа: {str(e)}")
        return None

def format_phone(phone):
    """Форматирование номера в формат +7XXXXXXXXXX"""
    # Очищаем от всех символов, кроме цифр
    cleaned = ''.join(filter(str.isdigit, str(phone)))
    
    if cleaned.startswith('8') and len(cleaned) == 11:
        # Номер в формате 8XXXXXXXXXX -> +7XXXXXXXXX
        return '+7' + cleaned[1:]
    elif len(cleaned) == 10:
        # Номер в формате XXXXXXXXXX -> +7XXXXXXXXXX
        return '+7' + cleaned
    else:
        # Возвращаем оригинал с префиксом +7
        return f'+7{cleaned[-10:]}'

def process_order(order_data, headers):
    """Обработка одного заказа"""
    try:
        # Извлечение данных
        customer_relation = order_data['data'][0]['relationships']['customer']
        customer_id = customer_relation['data']['id']
        order_attrs = order_data['data'][0]['attributes']
        
        # Поиск данных о клиенте
        customer_data = next(
            (item for item in order_data['included'] if item['type'] == 'customers'),
            None
        )
        
        # Форматирование телефона
        phone = customer_data['attributes']['phone'] if customer_data else "Без телефона"
        phone = format_phone(phone) if phone != "Без телефона" else phone
        
        # Получение бонусов
        bonus_points = get_customer_bonus(customer_id, headers)
        
        # Создание контакта
        contact_id = create_contact(
            name=customer_data['attributes']['title'] if customer_data else "Без имени",
            phone=phone,
            bonus_points=bonus_points
        )
        
        if contact_id:
            # Создание сделки
            return create_lead(
                name=f"Заказ {order_attrs['docNo']}",
                budget=order_attrs['totalAmount'],
                contact_id=contact_id,
                purchase_date=order_attrs['date']
            )
        return False
    except Exception as e:
        print(f"Ошибка обработки заказа: {str(e)}")
        return False

def main():
    """Основная логика программы"""
    # Авторизация в Posiflora
    posiflora_token = get_posiflora_token()
    if not posiflora_token:
        return

    headers = {
        "Authorization": f"Bearer {posiflora_token}",
        "Content-Type": "application/json"
    }

    # Получение общего количества заказов
    done_orders_count = get_done_orders_count(headers)
    if not done_orders_count:
        print("Нет завершенных заказов")
        return

    print(f"Найдено завершенных заказов: {done_orders_count}")

    # Обработка существующих заказов
    for i in range(1, done_orders_count + 1):
        print(f"Обработка заказа {i} из {done_orders_count}...")
        order_data = get_order_data(i, headers)
        if order_data:
            process_order(order_data, headers)

    # Мониторинг новых заказов
    print("\nЗапуск мониторинга новых заказов...")
    last_count = done_orders_count
    while True:
        # Проверяем токен перед каждым запросом
        if not posiflora_token:
            posiflora_token = get_posiflora_token()
            if not posiflora_token:
                print("Не удалось получить токен. Повторная попытка через 60 секунд...")
                time.sleep(60)
                continue
            headers["Authorization"] = f"Bearer {posiflora_token}"

        current_count = get_done_orders_count(headers)
        if current_count is None:
            print("Ошибка получения количества заказов. Повторная попытка через 60 секунд...")
            time.sleep(60)
            continue

        if current_count > last_count:
            print(f"Найдено новых заказов: {current_count - last_count}")
            
            for i in range(last_count + 1, current_count + 1):
                print(f"Обработка нового заказа {i}...")
                order_data = get_order_data(i, headers)
                if order_data:
                    process_order(order_data, headers)
            
            last_count = current_count
        
        time.sleep(60)

if __name__ == "__main__":
    main()