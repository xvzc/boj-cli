from cryptography.fernet import Fernet


def create_key():
    k = Fernet.generate_key()
    return k


def encrypt(k, p):
    f = Fernet(k)
    c = f.encrypt(bytes(p, 'utf-8'))
    return c


def decrypt(k, c):
    f = Fernet(k)
    p = f.decrypt(c).decode('utf-8')
    return p
