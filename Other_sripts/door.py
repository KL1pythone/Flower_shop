import tinytuya
import time

# Идентификационные данные
ACCESS_ID = '57ppxafxxk5c7dcvhjku'
ACCESS_KEY = '047256cc46ea457d8d67df22a407b941'
DEVICE_ID = 'bf7146db8a50f5ad71oft3'
REGION_KEY = "eu"  # Укажите соответствующий регион: "cn", "us", "eu", "in"

# Инициализация устройства
device = tinytuya.Cloud(
    apiRegion=REGION_KEY,
    apiKey=ACCESS_ID,
    apiSecret=ACCESS_KEY,
    apiDeviceID=DEVICE_ID
)

# Получение информации об устройстве (схема)
# device_info = device.getstatus(DEVICE_ID)
# device_schema = device.getdps(DEVICE_ID)

# print("==> Информация об устройстве:")
# print(device_info)
# print("\n==> Схема устройства:")
# print(device_schema)

def turn_on_lamp():
    result = device.sendcommand(DEVICE_ID, {'commands': [{'code': 'switch_1', 'value': True}]})
    print(result)
    return result['success']
    # time.sleep(10)
    # result = device.sendcommand(DEVICE_ID, {'commands': [{'code': 'switch_1', 'value': False}]})
    # return result['success']

def turn_off_lamp():
    result = device.sendcommand(DEVICE_ID, {'commands': [{'code': 'switch_1', 'value': False}]})
    # time.sleep(10)
    # result = device.sendcommand(DEVICE_ID, {'commands': [{'code': 'switch_1', 'value': True}]})
    print(result)
    return result['success']


while True:
    try:
        command = int(input("Введите команду: "))
        if command == 1:
            turn_on_lamp()
        elif command == 2:
            turn_off_lamp()
        else:
            print("Неверная команда. Пожалуйста, введите 1 или 2.")
    except ValueError:
        print("Пожалуйста, введите числовое значение.")