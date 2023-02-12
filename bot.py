import configparser
import json
import csv

from telethon.sync import TelegramClient

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest  # метод, позволяющий получить сообщения пользователей из чата и работать с ним
from telethon.tl.types import PeerChannel  # специальный тип, определяющий объекты типа «канал/чат», с помощью которого можно обратиться к нужному каналу для парсинга сообщений

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

# В urls.keys() можно передавать как ссылки так и id
urls = {'Yandex_Market': 'https://t.me/market_marketplace', 'OZON' : 'https://t.me/ozonmarketplace'}


async def dump_all_messages(channel, name, news_number):
        
    # Записывает JSON-файл с информацией о total_count_limit последних новостях с канала
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 1   # максимальное число записей, передаваемых за один раз

    all_messages = {name:{}}   # словарь всех сообщений
    total_messages = 0
    total_count_limit = news_number # поменяйте это значение, если вам нужны более 10 сообщений
    print(f'Парсим {name}')

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))

        if not history.messages:
            print('Нет истории сообщений')
            break

        messages = history.messages

        for message in messages:
            if message.photo:
                value = {message.id : (message.message, message.date, message.views, message.forwards, message.photo.id)}
                all_messages[name].update(value)
            else:
                value = {message.id : (message.message, message.date, message.views, message.forwards, 'None')}
                all_messages[name].update(value)

            # В случае, когда к сообщению прикреплена больше 1 картинки, каждая дополнительная считается отдельным сообщением со своим id
            if message.message == '':
                total_count_limit += 1

            # Если сообщение фото, то cохраняет фото в папку ./name под именем id сообщения
            if message.photo:
                print('File Name :' + str(message.photo.id))
                path = await client.download_media(message.media, f"./static/{name}/{message.photo.id}.jpg")
                print('File saved to', path)  # в случае успешного скачивания сообщает куда файл скачан

        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages[name])
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    class DateTimeEncoder(json.JSONEncoder):
        # Класс для сериализации записи дат в JSON
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)
    
    try:
        print('Ищу файл channel_messages.json')
        with open('channel_messages.json') as inf:    
            old_data = json.load(inf)
    except FileNotFoundError:
        print('Файл не найден')
        print('Создаю новый channel_messages.json')
        with open('channel_messages.json', 'w', encoding='utf8') as ouf:
            print("Сохраняем данные в файл...")
            json.dump(all_messages, ouf, ensure_ascii=False, cls=DateTimeEncoder) 
    else:
        print('Файл найден')
        data = old_data
        data.update(all_messages)
        with open('channel_messages.json', 'w', encoding='utf8') as ouf:
            print("Сохраняем данные в файл...")
            json.dump(data, ouf, ensure_ascii=False, cls=DateTimeEncoder)
            
    print(f'Парсинг новостей на канале {name} успешно выполнен.')
    print('*'* 60)

async def _main(news_number):
    # Запуск клиента
    await client.start()
    print("Клиент создан")
    print("*"*60)
    # Проверка на авторизацию
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Введите код: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Введите пароль: '))

    for key, url in urls.items():
        if url.isdigit():
            entity = PeerChannel(int(url))
        else:
            entity = url
        channel = await client.get_entity(entity)
        await dump_all_messages(channel, key, news_number)

def start_bot(news_number):
    with client:
        client.loop.run_until_complete(_main(news_number))


