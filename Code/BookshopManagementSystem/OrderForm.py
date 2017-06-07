class OrderForm(object):
    # bookname = ""
    # booknum = ""

    def __init__(self):
        self.bookname = ""  # 实例属性bookname
        self.booknum = 0

    def get_bookname(self):
        return self.bookname

    def get_booknum(self):
        return self.booknum

    def set_bookname(self, bookname):
        self.bookname = bookname

    def set_booknum(self, booknum):
        self.booknum = booknum


class ShopkeeperOrderForm(OrderForm):
    def __init__(self):
        self.bookname = ""
        self.booknum = 0
        self.bid = 0
        self.fix_price = 0

    def set_bid(self, bid):
        self.bid = bid

    def set_fix_price(self, fix_price):
        self.fix_price = fix_price


class CustomerOrderForm(OrderForm):
    def __init__(self):
        self.bookname = ""  # 实例属性bookname
        self.booknum = 0
        self.address = ""
        self.phonenum = ""
        self.cusname = ""

    def get_address(self):
        return self.address

    def get_phonenum(self):
        return self.phonenum

    def get_cusname(self):
        return self.cusname

    def set_address(self, address):
        self.address = address

    def set_cusname(self, cusname):
        self.cusname = cusname

    def set_phonenum(self, phonenum):
        self.phonenum = phonenum
