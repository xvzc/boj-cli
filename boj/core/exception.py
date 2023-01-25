class WrongAnswerException(Exception):
    def __init__(self):
        self.msg = ''

    def __str__(self):
        return self.msg

class LoginRequiredException(Exception):
    def __init__(self):
        self.msg = 'Login Required'

    def __str__(self):
        return self.msg
