import requests
import json

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
    response = requests.post(url, json=payload)
    return response.json()['data']['attributes']['accessToken']

def get_last_orders(headers, limit=10):
    url = f"https://cvetoot.posiflora.com/api/v1/orders?page[size]={limit}&filter[statuses]=done"
    response = requests.get(url, headers=headers)
    return response.json()

def get_customer_bonus(customer_id, headers):
    if not customer_id:
        return None
    url = f"https://cvetoot.posiflora.com/api/v1/customers/{customer_id}"
    response = requests.get(url, headers=headers)
    return response.json()['data']['attributes'].get('currentPoints')

def process_orders(orders_data, headers):
    results = []
    for order in orders_data['data']:
        try:
            # Проверяем наличие информации о клиенте
            if not order.get('relationships', {}).get('customer', {}).get('data'):
                print(f"⚠️ В заказе {order['id']} отсутствует информация о клиенте")
                continue
                
            customer_id = order['relationships']['customer']['data']['id']
            
            # Получаем бонусные баллы
            bonus = get_customer_bonus(customer_id, headers)
            
            # Формируем результат
            result = {
                "order_id": order['id'],
                "customer_id": customer_id,
                "bonus_points": bonus,
                "total_amount": order['attributes']['totalAmount'],
                "date": order['attributes']['date']
            }
            results.append(result)
            print(f"✅ Обработан заказ {order['id']}")
            
        except KeyError as e:
            print(f"❌ Ошибка в структуре данных заказа {order.get('id', 'unknown')}: {str(e)}")
        except Exception as e:
            print(f"🚨 Неожиданная ошибка при обработке заказа: {str(e)}")
    
    return results

def main():
    try:
        # Авторизация
        token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Получаем 10 последних заказов
        print("🔄 Получение последних заказов...")
        orders_data = get_last_orders(headers)
        
        # Обрабатываем заказы
        print("🔧 Обработка заказов...")
        processed_data = process_orders(orders_data, headers)
        
        # Сохраняем в файл
        with open('json_test.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Тестовые данные сохранены в json_test.json")
    
    except Exception as e:
        print(f"🔥 Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    main()