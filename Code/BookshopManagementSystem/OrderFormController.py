import OrderForm


class OrderFormController(object):
    # orderform = None

    def __init__(self):
        self.coflist = []  # 实例变量为列表, 存储顾客订单
        self.soflist = []  # 存储店主订单

    def set_shopkeeper_orderform(self, bookname, booknum):
        pass
        # self.orderform = OrderForm.ShopkeeperOrderForm(bookname, booknum)

    def set_customer_orderform(self, bookname, booknum):
        pass
        # self.orderform = OrderForm.CustomerOrderForm(bookname, booknum)

    def new_customer_orderform(self):
        cof = OrderForm.CustomerOrderForm()
        self.coflist.append(cof)
        return cof

    def new_shopkeeper_orderform(self):
        sof = OrderForm.ShopkeeperOrderForm()
        self.soflist.append(sof)
        return sof
