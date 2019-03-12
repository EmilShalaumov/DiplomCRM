class CrmUser:
    def __init__(self, username, password, lastlogin = "", token = "", publickey = "", tokenexpire = ""):
        self.username = username
        self.password = password
        self.lastlogin = lastlogin
        self.publickey = publickey
        self.token = token
        self.tokenexpire = tokenexpire