import base64
import hashlib
from random import randint

# following module: pip install pycryptodome
from Crypto import Random
from Crypto.Cipher import AES

# following module: to use django to manage SECRETS
# from django.conf import settings


# following secrets must be hidden
SECRET_KEY = 'secret'
SECRET_SEP = b'@..'  # too simple seperator can cause exception in decrpyt function: .split()


def make_key(secret_key: str) -> bytes:
    return hashlib.sha256(secret_key.encode('utf-8')).digest()


def pad(x: str, variance: int=None) -> str:
    if variance is None:
        variance = randint(1, 100)
    value = variance - len(x) % variance
    return x + chr(value) * value


def unpad(x: bytes) -> bytes:
    return x[:-x[-1]]


class AESCipher_CBC:
    """
    AES-128
    
    Example:
        raw = '1234567890'
        print(f"raw: {raw}")

        encrypted = AESCipher_CBC.encrypt(raw)
        print(f"encrypted: {encrypted} (length={len(encrypted)})")

        decrpyted = AESCipher_CBC.decrypt(encrypted)
        print(f"decrpyted: {decrpyted}")

        assert raw == decrpyted
    """
    BS = 16

    @classmethod
    def encrypt(cls, raw):
        iv = Random.get_random_bytes(cls.BS)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(pad(raw, cls.BS).encode())
        return base64.b64encode(SECRET_SEP.join([ciphertext, iv]))

    @classmethod
    def decrypt(cls, enc):
        ciphertext, iv = base64.b64decode(enc).split(SECRET_SEP)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(ciphertext)).decode()


class AESCipher_EAX:
    """
    AES-128

    Example:

        raw = '1234567890'
        print(f"raw: {raw}")

        encrypted = AESCipher_EAX.encrypt(raw)
        print(f"encrypted: {encrypted} (length={len(encrypted)})")

        decrpyted = AESCipher_EAX.decrypt(encrypted)
        print(f"decrpyted: {decrpyted}")

        assert raw == decrpyted
    """
    BS = 16

    @classmethod
    def encrypt(cls, raw):
        nonce = Random.get_random_bytes(cls.BS)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(pad(raw).encode())
        return base64.b64encode(SECRET_SEP.join([ciphertext, tag, nonce]))

    @classmethod
    def decrypt(cls, enc):
        ciphertext, tag, nonce = base64.b64decode(enc).split(SECRET_SEP)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_EAX, nonce=nonce)
        return unpad(cipher.decrypt_and_verify(ciphertext, tag)).decode()


class AESCipher_SIV:
    """
    AES-256

    Example:

        raw = '1234567890'
        print(f"raw: {raw}")

        encrypted = AESCipher_SIV.encrypt(raw)
        print(f"encrypted: {encrypted} (length={len(encrypted)})")

        decrpyted = AESCipher_SIV.decrypt(encrypted)
        print(f"decrpyted: {decrpyted}")

        assert raw == decrpyted
    """
    BS = 32

    @classmethod
    def encrypt(cls, raw):
        nonce = Random.get_random_bytes(cls.BS)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_SIV, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(pad(raw).encode())
        return base64.b64encode(SECRET_SEP.join([ciphertext, tag, nonce]))

    @classmethod
    def decrypt(cls, enc):
        ciphertext, tag, nonce = base64.b64decode(enc).split(SECRET_SEP)
        cipher = AES.new(make_key(SECRET_KEY), AES.MODE_SIV, nonce=nonce)
        return unpad(cipher.decrypt_and_verify(ciphertext, tag)).decode()
