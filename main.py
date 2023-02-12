import json
import sqlite3
from bot import start_bot


# Проверяем наличие json
def check_json(news_number):
    try:
        print('Ищу файл channel_messages.json')
        with open('channel_messages.json') as inf:
            data = json.load(inf)
    except FileNotFoundError:
        print('Файл не найден')
        print('Создаю новый channel_messages.json')
        start_bot(news_number)
        with open('channel_messages.json') as inf:
            data = json.load(inf)
        return data
    else:
        print('Файл найден')
        print('*'*60)
        return data
        

def create_db(name):
    # Создает таблицу с именeм name
    try:
        print('Создаю таблицу {name}')
        connection = sqlite3.connect("./db.sqlite3")
        print("Успешное соединение с SQLite")
        cursor = connection.cursor()
        table = f""" CREATE TABLE {name} (
                message_id INTEGER PRIMARY KEY,
                message TEXT,
                date DATETIME,
                views INTEGER,
                forwards INTEGER,
                path_to_photo TEXT
                ); """
        cursor.execute(table)
        print("Таблица создана")
    except  Exception as ex:
        print(ex) 
        print(f'Error in {create_db.__name__} function')
        if connection:
            connection.close()
            print("Соединение с  sqlite завершено")
    finally:
        if connection:
            connection.close()
            print("Соединение с  sqlite завершено")


def count_news(data, news_number):
    try:
        names = list(data.keys())
        old_news_number = len(data[names[0]])
        if old_news_number != news_number:
            start_bot(news_number)
            data = check_json(news_number)
    except  Exception as ex:
        print(ex) 
        print(f'Error in {count_news.__name__} function')
    else:
        print(f'Количество записей изменено, было {old_news_number}, стало {news_number}')
        return data

def fill_db(data, name):
    # Заполняет таблицу name

    message_list = list(data[name].keys())

    for message in message_list:
        try:
            print(f'Вносим данные в {name}')
            connection = sqlite3.connect("./db.sqlite3")
            print("Успешное соединение с SQLite")
            cursor = connection.cursor()
            insert = (message, data[name][message][0],
                          data[name][message][1], data[name][message][2], 
                          data[name][message][3], f'/static/{name}/{data[name][message][4]}.jpg')           
            cursor.execute(f""" INSERT INTO {name} values(?,?,?,?,?,?)""", insert)
            connection.commit()
            print(f"Данные сообщения {message} внесены в {name}")
        except  Exception as ex:
            print(ex) 
            print(f'Error in {fill_db.__name__} function')
            if connection:
                connection.close()
                print("Соединение с  sqlite завершено")
        finally:
            if connection:
                connection.close()
                print("Соединение с  sqlite завершено")


def db_check(data):
    # Проверяем таблицы
    try:
        connection = sqlite3.connect("./db.sqlite3")
        print("Успешное соединение с SQLite")
        sql_query = """SELECT name FROM sqlite_master  
            WHERE type='table';"""

        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor()

        list_of_tables = cursor.execute(sql_query).fetchall()
        print('Есть таблицы:', ", ".join(list_of_tables))
        list_of_markets = list(data.keys())
        print('Маркеты:', ", ".join(list_of_markets))

        for name in list_of_markets:
            if name not in list_of_tables:
                print(f'Таблица {name} не создана')
                if connection:
                    connection.close()
                    print("Соединение с  sqlite завершено")
                create_db(name)
                fill_db(data, name)
            else:
                print(f'Таблица {name} есть')
                fill_db(data, name) 
    except sqlite3.Error as error:
        print("Ошибка исполнения запроса", error)
    finally:
        if connection:
            connection.close()
            print("Соединение с  sqlite завершено")


def main():
    print('Сколько новостей нужно?')
    news_number = int(input('Введите количество новостей цифрами \n'))
    data = check_json(news_number)
    data = count_news(data, news_number)
    db_check(data)

if __name__ == "__main__":
    main()
