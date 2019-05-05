import hashlib


def hash_password(password, salt):
    p = hashlib.md5()
    if isinstance(password, str):
        p.update(password.encode('utf-8'))
    elif isinstance(password, bytes):
        p.update(password)
    else:
        # TODO raise
        pass

    if isinstance(salt, str):
        p.update(salt.encode('utf-8'))
    elif isinstance(salt, bytes):
        p.update(salt)
    else:
        # TODO raise
        pass

    r = p.hexdigest()
    return r
