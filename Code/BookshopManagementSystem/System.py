import AccountController
import BookController
import OrderFormController
import DataController


class System(object):
    # ac = None
    # bc = None
    # ofc = None

    def __init__(self):
        self.ac = AccountController.AccountController()
        self.bc = BookController.BookController()
        self.ofc = OrderFormController.OrderFormController()
        self.dc = DataController.DataController()


