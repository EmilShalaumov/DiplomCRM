from pymongo import MongoClient
from Model.CrmUser import CrmUser
import secrets
import datetime
import time

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
        #expiredatehere
        #time.strftime('%x %H:%M')
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




dba = DatabaseAdapter('localhost', 27017)
#print(dba.createUser("Vova", "123456"))
#print(dba.logIn("Emil", "123456"))
token = dba.logIn('Vova', '123456')
print(token)
print(dba.validateToken(token))

