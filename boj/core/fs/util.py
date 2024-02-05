import os


def mkdir(path: str, exist_ok=True):
    try:
        os.makedirs(name=path, exist_ok=exist_ok)
    except OSError as e:
        raise e


def file_exists(path: str):
    if os.path.isfile(path):
        return True
    return False
