class TokenNotFoundExeption(Exception):
    def __init__(self, name) -> None:
        self.name = name
        self.message = f'Token not found {name}'
        super().__init__(self.message)


class TelegramChatUnavailableExeption(Exception):
    def __init__(self) -> None:
        self.message = 'Telegram chat unavailable.'
        super().__init__(self.message)


class APIResponseStructureExeption(Exception):
    def __init__(self) -> None:
        self.message = 'API structure error. Keys not found.'
        super().__init__(self.message)


class WrongHomeworkStatusExeption(Exception):
    def __init__(self) -> None:
        self.message = 'Unexpected homework status'
        super().__init__(self.message)
