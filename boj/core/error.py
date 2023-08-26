from boj.core.base import BojError


class AuthenticationError(BojError):
    def __init__(self):
        super().__init__("Authentication failed.")


class HttpError(BojError):
    def __init__(self, url):
        super().__init__(f'Error while calling remote service: {url}')


class IllegalStatementError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class ParsingConfigError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class FileIOError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class RunCodeError(BojError):
    def __init__(self, msg):
        super().__init__(msg)
