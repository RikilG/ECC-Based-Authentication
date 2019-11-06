import hashlib
import random
from CryptoWrapper import eccEncrypt, eccDecrypt


def gen_hash(x, a="", b="", c=""):
    # concatenate all parameters
    x = str(x) + str(a) + str(b) + str(c)
    x = str.encode(x)
    x = hashlib.sha256(x).hexdigest()
    return x


def gen_randint(h_limit=2**8-1):
    return random.randint(0, h_limit)


def encrypt(key, data1, data2, data3, data4, data5):
    return eccEncrypt(key, curve, data)


def decrypt():
    return eccDecrypt(privKey, curve, data)


def gen_sig(PK, data):
    pass


def verify_sig(PK, data):
    pass