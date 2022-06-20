from hashlib import md5


def encrypt_plaintext_password(password: str, salt: str, rounds=1):
    result = password
    while rounds > 0:
        result = salt + result + salt
        result = md5(result.encode("utf-8")).hexdigest()
        rounds -= 1
    return result
