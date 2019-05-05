import md5


def hash_password(password, salt):
    p = md5.new()
    p.update(password)
    p.update(salt)

    r = p.hexdigest()
    return r
