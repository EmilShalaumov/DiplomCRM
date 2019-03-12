from pymongo import MongoClient
from Model.CrmUser import CrmUser
import secrets
import datetime
import time
import EDC

class DatabaseAdapter:
    databaseName = 'CRMDB'
    usersCollection = 'users'
    tokenTime = 30

    def __init__(self, address, port):
        self.client = MongoClient(address, port)
        self.db = self.client[self.databaseName]

    def createUser(self, username, password):
        users = self.db[self.usersCollection]
        crmUser = CrmUser(username, password)
        findUser = users.find_one({"username": username})
        if findUser is None:
            userId = users.insert_one(crmUser.__dict__).inserted_id
            token = self.generateToken(users, userId)
            return token
        print('User with name ' + username + ' already exists.')
        return False
    
    def logIn(self, username, password):
        users = self.db[self.usersCollection]
        user = users.find_one({"username": username, "password": password})
        if user is None:
            return False
        return self.generateToken(users, user['_id'])

    def generateToken(self, users, userId):
        token = secrets.token_hex(16)
        tokenExpire = datetime.datetime.now() + datetime.timedelta(minutes=self.tokenTime)
        print(tokenExpire)
        users.update_one({"_id": userId}, { "$set": {"token": token, "tokenexpire": tokenExpire}})
        return token

    def validateToken(self, token):
        users = self.db[self.usersCollection]
        user = users.find_one({"token": token})
        if user is None or user['tokenexpire']  < datetime.datetime.now():
            return False
        return user
    
    def generateKeyPair(self, token):
        user = self.validateToken(token)
        if user == False:
            return False
        edc = EDC.EDC()
        #users = self.db[self.usersCollection]
        (pubkey, privkey) = edc.generateKeyPair()
        #users.update_one({"_id": user['_id']}, {"$set": {"publickey": pubkey}})
        return (pubkey, privkey)
        




dba = DatabaseAdapter('localhost', 27017)
#print(dba.createUser("Vova", "123456"))
#print(dba.logIn("Emil", "123456"))
#token = dba.logIn('Vova', '123456')
#print(token)
#print(dba.validateToken(token))
print(dba.generateKeyPair('8de0d79191acef966e3f513503f26fd4'))

