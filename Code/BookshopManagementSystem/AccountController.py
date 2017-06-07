import Account


class AccountController(object):
    # account = None

    def get_account(self):
        return self.account

    def new_account(self, usertype):
        if usertype == '1':
            self.account = Account.ShopkeeperAccount()
        elif usertype == '2':
            self.account = Account.CustomerAccount()
        elif usertype == '3':
            self.account = Account.SupplierAccount()

    def __init__(self):
        self.account = None
        # self.set_account(username, password)
