import hashlib


def hash_password(password, salt):
    p = hashlib.md5()
    p.update(password)
    p.update(salt)

    r = p.hexdigest()
    return r
