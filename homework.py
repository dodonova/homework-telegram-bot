import os
import logging
import requests
import time
from http import HTTPStatus
from json.decoder import JSONDecodeError

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

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
# To test how bot works set START_PERIOD longer:
START_PERIOD = 24 * 60 * 60

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
    """Check tokens for Practicum API, Telegram API and Chat ID."""
    token_names = ['PRACTICUM TOKEN', 'TELEGRAM CHAT ID', 'TELEGRAM TOKEN']
    tokens = [PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN]
    for token_name, token in zip(token_names, tokens):
        if token is None:
            logger.critical(f'There is no token {token_name}.')
            return False
    return True


def send_message(bot, message):
    """Send  textmessage from bot to chat TELEGRAM_CHAT_ID."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Message sent:"{message}"')
    except TelegramError:
        logger.exception('Send error. Message:"{message}"')


def check_telegram_chat(bot):
    """Checks the availability of a telegram chat."""
    response = requests.get(TELEGRAM_ENDPOINT)
    if response.status_code == HTTPStatus.OK:
        return True
    else:
        logger.error("Error occurred while checking chat ID")
        return False


def get_api_answer(timestamp):
    """Get answer from Practicum API."""
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    payload = {'from_date': int(timestamp)}
    try:
        homework_statuses = requests.get(
            url=ENDPOINT,
            headers=headers,
            params=payload
        )
        logger.debug('Practicum API response received')
    except Exception as error:
        logger.error(f"Practicum API failed connection: {error}")
        return
    logger.debug(
        f"Practicum API request status code: {homework_statuses.status_code}.")
    if homework_statuses.status_code != HTTPStatus.OK:
        logger.error('Endpoint is unavailable.')
        raise requests.HTTPError()
    try:
        homework_json = homework_statuses.json()
        logger.debug('Response has JSON format.')
        return homework_json
    except JSONDecodeError:
        logger.error('Wrong response format:  it is not JSON.')


def check_response(response):
    """Check structure of response from Practicum API."""
    # if response is None:
    #     return False
    if not isinstance(response, dict):
        logger.error('Response is not a dictionary.')
        raise TypeError('Response is not a dictionary.')
    if 'homeworks' not in response:
        raise APIResponseStructureExeption
    hw = response.get('homeworks')
    logger.debug(f"Homeworks type: {type(hw)}")
    if not isinstance(hw, list):
        raise TypeError
    if len(hw) == 0:
        # logger.debug('No new statuses.')
        return True
    if all(key in hw[0] for key in [
        # 'date_updated',
        # 'id',
        'status',
        'homework_name',
        # 'lesson_name',
        # 'reviewer_comment'
    ]):
        return True
    else:
        logger.error('API keys not found.')
        raise APIResponseStructureExeption

    return False


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


class TelegramHandler(logging.StreamHandler):
    """Handler to send logger messages to the telegram chatbot."""

    last_error = ''

    def __init__(self, bot) -> None:
        """The bot object should be passed to the constructor."""
        super().__init__()
        self.bot = bot

    def emit(self, record):
        """Congfigure sending message for Telegram Handler."""
        log_entry = self.format(record)
        if TelegramHandler.last_error != log_entry:
            TelegramHandler.last_error = log_entry
            try:
                self.bot.send_message(TELEGRAM_CHAT_ID, log_entry)
            except Exception:
                super().emit(log_entry)


def main():
    """Main bot logic."""
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format=(
            '\n[%(levelname)s] %(asctime)s  - '
            '(%(filename)s).%(funcName)s:%(lineno)d. %(message)s'),
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()]
    )
    if not check_tokens():
        raise TokenNotFoundExeption

    bot = Bot(token=TELEGRAM_TOKEN)
    if not check_telegram_chat(bot):
        raise TelegramChatUnavailableExeption

    tg_handler = TelegramHandler(bot)
    tg_handler.setLevel(logging.ERROR)
    # tg_handler.setFormatter(formatter)
    logger.addHandler(tg_handler)

    messages_log = set()

    while True:
        timestamp = int(time.time())
        time_before = timestamp - START_PERIOD
        message = None
        total_messages = len(messages_log)
        try:
            response = get_api_answer(time_before)
            if check_response(response):
                for homework in response.get('homeworks'):
                    message = parse_status(homework)
                    if message not in messages_log:
                        send_message(bot, message)
                        messages_log.add(message)
                if len(messages_log) == total_messages:
                    logger.debug("No new homework statuses.")
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
