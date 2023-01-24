class WrongAnswerException(Exception):
    def __init__(self):
        self.msg = ''

    def __str__(self):
        return self.msg
