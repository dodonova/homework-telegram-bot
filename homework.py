import os
import logging
import requests
import time
from dotenv import load_dotenv
from json.decoder import JSONDecodeError
from telegram import Bot
from telegram.error import TelegramError
from http import HTTPStatus

from exeptions import (
    APIResponseStructureExeption,
    WrongHomeworkStatusExeption,
    TokenNotFoundExeption,
    TelegramChatUnavailableExeption
)


load_dotenv()

logger = logging.getLogger('telegram_logger')

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
START_PERIOD = 0
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
TELEGRAM_ENDPOINT = (f'https://api.telegram.org/'
                     f'bot{TELEGRAM_TOKEN}/getChat?chat_id={TELEGRAM_CHAT_ID}')
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    ...


def send_message(bot, message):
    ...


def get_api_answer(timestamp):
    ...


def check_response(response):
    ...


def parse_status(homework):
    """Define status og homework and generate message for student."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise APIResponseStructureExeption
    verdict = HOMEWORK_VERDICTS.get(homework.get('status'))
    if verdict is None:
        logger.error('Unexpected homework status')
        raise WrongHomeworkStatusExeption
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    ...

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    ...

    while True:
        try:

            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
