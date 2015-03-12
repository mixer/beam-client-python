class AuthenticationFailedError(Exception):
    pass

class ResponseError(Exception):
    def __init__(self, response):
        super(ResponseError, self)
        self.response = response

class NotAuthenticatedError(ResponseError):
    pass
class UnknownCodeError(ResponseError):
    pass

