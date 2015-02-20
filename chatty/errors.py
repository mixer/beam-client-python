class RequestError(Exception):
    def __init__(self, response):
        self.response = response


# This error is thrown when we fail to connect to the Beam server.
class NotAuthenticatedError(RequestError):
    pass


# Thrown if there's an error and we don't know why!
class UnknownError(RequestError):
    pass
