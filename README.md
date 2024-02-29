# Homework Bot
Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнавать статус домашней работы студента: взята ли работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

- раз в 10 минут бот опрашивает API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправлять студенту соответствующее уведомление в Telegram;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

### Статусы домашней работы
Статус домашки (значение по ключу status ) может быть трёх типов:
- reviewing: работа взята в ревью;
- approved: ревью успешно пройдено;
- rejected: в работе есть ошибки, нужно поправить.
Если домашку ещё не взяли в работу — её не будет в выдаче.


### Установка и запуск

Для локального запуска бота: клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Belyanski/homework-telegram-bot
```
```
cd homework-telegram-bot
```
В этой же папке создать файл `.env` в котором разместить информацию о переменных окружения.

Пример в файле [.env.example](./.env.example)


PRACTICUM_TOKEN можно получить по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a

TELEGRAM_TOKEN можно получить при создании нового бота с помощью телеграм бота https://t.me/botfather

TELEGRAM_CHAT_ID - это ID чата пользователя, можно получить c помощью бота https://t.me/userinfobot 



- Cоздать и активировать виртуальное окружение
```
python -m venv venv # Для Windows
python3 -m venv venv # Для Linux и macOS
```
```
source venv/Scripts/activate # Для Windows
source venv/bin/activate # Для Linux и macOS
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Перейти в папку со скриптом управления и выполнить миграции
```
cd api_yamdb
```
```
python manage.py migrate
```

- Запустить проект
```
python manage.py runserver
```
