from cryptography.fernet import Fernet


def create_key():
    k = Fernet.generate_key()
    return k


def encrypt(k, p):
    f = Fernet(k)
    c = f.encrypt(p)
    return c


def decrypt(k, c):
    f = Fernet(k)
    p = f.decrypt(c)
    return p
