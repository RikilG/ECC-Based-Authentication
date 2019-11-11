import os
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

class CryptoWrapper():

    '''AES Cipher Specifics'''
    blockSize = 16          #Block Size
    keySize = 32            #keySize in Bytes - 32 bytes = 256bit Encryption
    mode = AES.MODE_CBC     #Cipher Block Mode
    
    def __init__(self):
        pass

    def __generateAESKeystring__(self):
        '''Generates Pseudo Random AES Key and Base64 Encodes Key - Returns AES Key'''
        key = os.urandom(self.keySize)
        keyString = base64.urlsafe_b64encode(key)
        return keyString
        
    def __extractAESKey__(self, keyString):
        '''Extracts Key from Base64 Encoding'''
        key = base64.urlsafe_b64decode(keyString)
        key = key[-32:]
        if len(key) != self.keySize:
            print(f"problem with key len: {len(key)}")
            raise Exception('Error: Key Invalid')
            os._exit(1)
        return key
    
    def __extractCrypto__(self, encryptedContent):
        '''Decodes Base64 Encoded Crypto'''
        cipherText = base64.urlsafe_b64decode(encryptedContent)
        return cipherText
    
    def __encodeCrypto__(self, encryptedContent):
        '''Encodes Crypto with Base64'''
        encodedCrypto = base64.urlsafe_b64encode(encryptedContent)
        return encodedCrypto
    
    def aesEncrypt(self, key, data):
        '''Encrypts Data w/ pseudo randomly generated key and base64 encodes cipher - Returns Encrypted Content and AES Key'''
        # key = self.__generateAESKeystring__()
        encryptionKey = self.__extractAESKey__(key)
        pad = self.blockSize - len(data) % self.blockSize
        data = data + pad * chr(pad)
        data = str.encode(data)
        iv = os.urandom(self.blockSize)
        cipherText = AES.new(encryptionKey, self.mode, iv).encrypt(data)
        encryptedContent = iv + cipherText
        encryptedContent = self.__encodeCrypto__(encryptedContent)
        return encryptedContent

    def aesDecrypt(self, key, data):
        '''Decrypts AES(base64 encoded) Crypto - Returns Decrypted Data'''
        decryptionKey = self.__extractAESKey__(key)
        encryptedContent = self.__extractCrypto__(data)
        iv = encryptedContent[:self.blockSize] 
        cipherText = encryptedContent[self.blockSize:]
        plainTextwithpad = AES.new(decryptionKey, self.mode, iv).decrypt(cipherText)
        # print(type(plainTextwithpad[-1]))
        if type(plainTextwithpad[-1]) is int:
            pad = plainTextwithpad[-1]
        else:
            pad = ord(plainTextwithpad[-1])
        plainText = plainTextwithpad[:-pad]
        # print(plainText)
        return plainText
    
    # def generateRSAKeys(self,keyLength):
    #     '''Generates Public/Private Key Pair - Returns Public / Private Keys'''
    #     private = RSA.generate(keyLength)
    #     public  = private.publickey()
    #     privateKey = private.exportKey()
    #     publicKey = public.exportKey()
    #     return privateKey, publicKey
    
    # def rsaPublicEncrypt(self, pubKey, data):
    #     '''RSA Encryption Function - Returns Encrypted Data'''
    #     publicKey = RSA.importKey(pubKey)
    #     encryptedData = publicKey.encrypt(data,'')
    #     return encryptedData
         
    # def rsaPrivateDecrypt(self, privKey, data):
    #     '''RSA Decryption Function - Returns Decrypted Data'''
    #     privateKey = RSA.importKey(privKey)
    #     decryptedData = privateKey.decrypt(data)
    #     return decryptedData
    
    # def rsaSign(self, privKey, data):
    #     '''RSA Signing - Returns an RSA Signature'''
    #     privateKey = RSA.importKey(privKey)
    #     if privateKey.can_sign() == True:
    #         digest = SHA256.new(data).digest()
    #         signature = privateKey.sign(digest,'')
    #         return signature
    #     else:
    #         raise Exception("Error: Can't Sign with Key")
        
    # def rsaVerify(self, pubKey, data, signature):
    #     '''Verifies RSA Signature based on Data received - Returns a Boolean Value'''
    #     publicKey = RSA.importKey(pubKey)  
    #     digest = SHA256.new(data).digest()
    #     return publicKey.verify(digest, signature)

    def eccGenerate(self):
        '''Generates Elliptic Curve Public/Private Keys'''
        privateKey = ECC.generate(curve='P-256')
        publicKey = privateKey.public_key()
        return privateKey, publicKey
    
    # def eccEncrypt(self,publicKey, curve, data):
    #     '''Encrypts Data with ECC using public key'''
    #     ecc = ECC(1, public=publicKey, private='', curve=curve)
    #     encrypted = ecc.encrypt(data)
    #     return encrypted
    
    # def eccDecrypt(self,privateKey, curve, data):
    #     '''Decrypts Data with ECC private key'''
    #     ecc = ECC(1, public='', private=privateKey, curve=curve)
    #     decrypted = ecc.decrypt(data)
    #     return decrypted
    
    def eccSign(self, privateKey, data):
        '''ECC Signing - Returns an ECC Signature'''
        h = SHA256.new(data.encode())
        signer = DSS.new(privateKey, 'fips-186-3')
        signature = signer.sign(h)
        return signature
        
    def eccVerify(self, publicKey, data, signature):
        '''Verifies ECC Signature based on Data received - Returns a Boolean Value'''
        h = SHA256.new(data.encode())
        verifier = DSS.new(publicKey, 'fips-186-3')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False


        
if __name__ == '__main__':
    '''Usage Examples'''
    
    print( '''

            Python Crypto Wrapper - By Chase Schultz
            
            Currently Supports: AES-256, RSA Public Key, RSA Signing, ECC Public Key, ECC Signing
            
            Dependencies: pyCrypto - https://github.com/dlitz/pycrypto
                          PyECC - https://github.com/rtyler/PyECC
            
            ''' )
      
    '''Instantiation of Crypto Wrapper and Message'''
    crypto = CryptoWrapper();
    message = 'Crypto Where art Thou... For ye art a brother...'
    print(f'Message to be Encrypted: {message}\n')
    
    
    '''AES ENCRYPTION USAGE'''
    '''***Currently Supporting AES-256***'''
    encryptedAESContent, key = crypto.aesEncrypt(message)
    print(f'Encrypted AES Message: {key}\nEncrypted with Key: {encryptedAESContent}')
    decryptedAESMessage = crypto.aesDecrypt(key, encryptedAESContent)
    print(f'\nDecrypted AES Content: {decryptedAESMessage}\n')


    '''RSA ENCRYPTION USAGE'''
    privateKey, publicKey = crypto.generateRSAKeys(2048)
    
    encryptedRSAContent = crypto.rsaPublicEncrypt(publicKey, message)
    print(f'Encrypted RSA Message with RSA Public Key: {encryptedRSAContent}\n')
    decryptedRSAMessage = crypto.rsaPrivateDecrypt(privateKey, encryptedRSAContent)
    print(f'\nDecrypted RSA Content with RSA Private Key: {decryptedRSAMessage}\n')
    
    
    '''RSA SIGNING USAGE'''
    signature = crypto.rsaSign(privateKey, message)
    print(f'Signature for message is: {signature}\n')
    if crypto.rsaVerify(publicKey, message, signature) is False:
        print('Could not Verify Message\n' )
    else:
        print('Verified RSA Content\n')
        
    '''ECC ENCRYPTION USAGE'''
    eccPrivateKey, eccPublicKey, eccCurve = crypto.eccGenerate()
    
    encryptedECCContent = crypto.eccEncrypt(eccPublicKey, eccCurve , message)
    print(f'Encrypted ECC Message with ECC Public Key: {encryptedECCContent}\n')
    decryptedECCContent = crypto.eccDecrypt(eccPrivateKey, eccCurve, encryptedECCContent)
    print(f'Decrypted ECC Content with ECC Private: {decryptedECCContent}\n')
    
    '''ECC SIGNING USAGE'''
    signature = crypto.eccSign(eccPrivateKey, eccCurve, message)
    print(f'Signature for message is: {signature}\n')
    if crypto.eccVerify(eccPublicKey, eccCurve, message, signature) is False:
        print('Could not Verify Message\n')
    else:
        print('Verified ECC Content\n')
    
    
    