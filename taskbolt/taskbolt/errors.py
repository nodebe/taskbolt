class UserError(Exception):
    def __init__(self, message='An error occured', code='400'):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message

class ServerError(Exception):
    def __init__(self, message='Internal Server error!', code='500'):
        self.message = message
        self.code = code