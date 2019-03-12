import hashlib
import rsa

class EDC:
    hashAlg = 'MD5'
    keySize = 512

    def __init__(self, hashAlg, keySize):
        self.hashAlg = hashAlg

    def generateKeyPair(self):
        return rsa.newkeys(self.keySize)

    def makeSignature(self, sourceString, privKey):
        return rsa.sign(sourceString, privKey, self.hashAlg)

    def verifySignature(self, sourceString, sigString, pubKey):
        try:
            rsa.verify(sourceString, sigString, pubKey)
        except rsa.VerificationError:
            return False
        return True


