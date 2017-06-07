class Message(object):
    def __init__(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
