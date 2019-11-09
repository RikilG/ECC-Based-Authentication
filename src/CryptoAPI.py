import hashlib
import random
from CryptoInternals import CryptoWrapper


def gen_hash(x, a="", b="", c=""):
    """generate hash of the string after conatenating all parameters
    """
    # concatenate all parameters
    if type(a) is list:
        if type(a[0]) is bytes:
            a = b' '.join(a)
        else:
            a = ' '.join(a)
    x = str(x) + str(a) + str(b) + str(c)
    x = str.encode(x)
    x = hashlib.sha256(x).hexdigest()
    return x


def gen_randint(h_limit=2**8-1):
    """generate a random integer between 0 and h_limit
    """
    return random.randint(0, h_limit)


def encrypt(key, data_list):
    """encrypt each term in data_list using given key and return the list 
    of encrypted values
    """
    crypto = CryptoWrapper()
    cipher_list = list()
    for data in data_list:
        data = str(data)
        # print(f"data: {data}")
        cipher_list.append( crypto.aesEncrypt(key, data) )
    return cipher_list

def decrypt(key, cipher_list):
    """decrypt each term in cipher_list using given key and return the list 
    of plain text values 
    """
    crypto = CryptoWrapper()
    data_list = list()
    for cipher in cipher_list:
        data_list.append( crypto.aesDecrypt(key, cipher) )
    return tuple(data_list)


def gen_sig_keys():
    """generate a private key for use with ECC signature function
    """
    crypto = CryptoWrapper()
    return crypto.eccGenerate()


def gen_sig(PR_key, data):
    """generate signature for given data using the given private key
    """
    crypto = CryptoWrapper()
    return crypto.eccSign(PR_key, data)


def verify_sig(PU_key, data, signature):
    """verify if the data matches with the signature
    """
    crypto = CryptoWrapper()
    return crypto.eccVerify(PU_key, data, signature)