Simple parser for telegram channels and some django backend for parsed messaged in AdminLTE v3 template


Just do `python main.py`

#### bot.py is a parser
For proper work bot.py requires `config.ini` in same folder,


example of config.ini

- [Telegram]
- api_id = your_api
- api_hash = your_hash
- username = your_username


bot.py will parse 10 (could be changed) last messages on given channels (url or id) and save data as json


main.py load json to db.sqlite3 (could be changed)


Loaded data could be read from admin pannel in started django server localhost:8000/admin/

#### Screencast

![alt text](https://github.com/qquppsala/tgparser-djangoback/blob/master/screencast.gif?raw=true)
