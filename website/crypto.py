import base64
import hashlib
from cryptography.fernet import Fernet

def getcipher(key):
    h = hashlib.sha256(key.encode()).digest()
    k = base64.urlsafe_b64encode(h)
    return Fernet(k)

def encryptbytes(data, key):
    f = getcipher(key)
    return f.encrypt(data)

def decryptbytes(data, key):
    f = getcipher(key)
    try:
        return f.decrypt(data)
    except Exception:
        return data
