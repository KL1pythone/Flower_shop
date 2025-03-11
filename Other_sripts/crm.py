import requests

SUBDOMAIN = 'cvetoot'
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjM5NDllYzBjZmYzM2JhYjE3MDQ4NGQxYTRjYWM3YmMwNWQwZGU1NWFmY2E1MmYwMjIxZTZlYTNkNzlmODRjNTBlZGMzNzIwNTVmMDk0MGYyIn0.eyJhdWQiOiI3YWNiYzgwNS1kNTIxLTQ4ZmEtODgzYS1kYTkzOWIxN2ZmN2MiLCJqdGkiOiIzOTQ5ZWMwY2ZmMzNiYWIxNzA0ODRkMWE0Y2FjN2JjMDVkMGRlNTVhZmNhNTJmMDIyMWU2ZWEzZDc5Zjg0YzUwZWRjMzcyMDU1ZjA5NDBmMiIsImlhdCI6MTc0MTAwODcyMCwibmJmIjoxNzQxMDA4NzIwLCJleHAiOjE4NjcxOTA0MDAsInN1YiI6Ijg1MDM0MTQiLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzAzNjU2NzcsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbImNybSIsImZpbGVzIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyIsInB1c2hfbm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiI0NWFlNDhkZS0xY2RjLTQzMDktYTNjOS1mY2E5NmNjNGFjODgiLCJhcGlfZG9tYWluIjoiYXBpLWIuYW1vY3JtLnJ1In0.RJJXQuLJzL7FT-U16FiOdhE-FsLJ2GCv6QxU8YaeuVaLjAr4wXkBeejgN4HgPXubN3PMVcN7D4U83po4lldLmi6_v6sj_2UnvYSOmmE8JJC6vF7oqXYq1q__la2E2v2ImVTlhfWW-shppE-J0CN3lGJlj0HFRNEPeYCJy1Oyb_Zs7IaVhaaCSBdDzGafPUhIdYiofDramgnBgribgIAmPZJEWyzCFxX58dCoNFH5dWn5oVDwM-UhIBjpt4Zx1UAuU7orQxZ15cZloSKKwfvA7lYLOsjfbXcdpdbIABjlji9z-QR1CY7EAqk5sb1z0lZmUfWlzWyvk6FPYgcFhq072w'
BASE_URL = f'https://{SUBDOMAIN}.amocrm.ru/api/v4'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def create_contact(name, phone, info):
    """Создание контакта с именем и телефоном"""
    contact_data = {
        "name": name,
        "custom_fields_values": [
            {
                "field_id": 568643,  # ID поля "Телефон"
                "values": [{"value": phone, "enum_id": 381257}]  # Укажите тип телефона
            },
            {
                "field_id": 1421111,  # ID поля "Телефон"
                "values": [{"value": info}]  # Укажите тип телефона
            }
        ]
    }

    try:
        response = requests.post(
            f'{BASE_URL}/contacts',
            headers=headers,
            json=[contact_data]
        )
        response.raise_for_status()
        # Исправлено получение ID контакта
        return response.json()['_embedded']['contacts'][0]['id']
    except Exception as e:
        print(f"Ошибка при создании контакта: {e}")
        print("Ответ сервера:", response.text)
        return None

def create_lead(name, price, contact_id, custom_fields):
    """Создание сделки с привязкой контакта"""
    lead_data = {
        "name": name,
        "price": price,
        "_embedded": {
            "contacts": [{
                "id": contact_id,
                "is_main": True  # Добавьте это поле
            }]
        },
        "custom_fields_values": custom_fields 
    }

    try:
        response = requests.post(
            f'{BASE_URL}/leads',
            headers=headers,
            json=[lead_data]
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при создании сделки: {e}")
        print("Детали ошибки:", response.text)
        return None

if __name__ == "__main__":
    # Сначала создаем контакт
    contact_id = create_contact(
        name="Кирилл",
        phone="+79123456789",
        info='Завершенно'
    )
        
    # Кастомные поля для сделки
    custom_fields = [
        {
            "field_id": 1387641,  # Дата покупки
            "values": [{"value": "03.03.2025"}]
        }
    ]
    
    # Создаем сделку
    new_lead = create_lead(
        name="Posiflora_Test",
        price=1000,
        contact_id=contact_id,
        custom_fields=custom_fields
    )

    if new_lead:
        print("Сделка успешно создана!")
    else:
        print("Не удалось создать сделку")