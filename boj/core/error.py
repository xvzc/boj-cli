class BojError(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class FatalError(BojError):
    def __init__(self, msg):
        super().__init__("fatal: " + msg)


class AuthenticationError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class DeprecatedError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class HttpError(BojError):
    def __init__(self, url):
        super().__init__(f"Error while calling http request: {url}")


class ParsingHtmlError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class IllegalStatementError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class ResourceNotFoundError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class FileSearchError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class ParsingConfigError(BojError):
    def __init__(self, query):
        super().__init__(query)


class FileIOError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class RunCodeError(BojError):
    def __init__(self, msg):
        super().__init__(msg)


class WebSocketError(BojError):
    def __init__(self, msg):
        super().__init__(msg)
