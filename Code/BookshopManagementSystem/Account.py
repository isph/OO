class Account(object):
    # ID = ""
    # email = ""
    # userName = ""
    # password = ""
    # money = 0

    def __init__(self):
        self.id = ""
        self.type = ""
        self.email = ""
        self.username = ""
        self.password = ""
        self.money = 0.0

    # def __init__(self, username, password, money=100):
    #    self.username = username
    #    self.password = password
    #    self.money = money

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def get_money(self):
        return self.money

    def get_password(self):
        return self.password

    def set_money(self, money):
        self.money = money

    def set_type(self, usertype):
        self.type = usertype

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password


class ShopkeeperAccount(Account):
    pass


class CustomerAccount(Account):
    pass


class SupplierAccount(Account):
    pass

