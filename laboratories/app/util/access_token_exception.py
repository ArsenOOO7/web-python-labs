class AccessTokenException(Exception):
    """ Raised when something wrong with JWT Token """

    def __init__(self, message, response_code: int = 401):
        self.response_code = response_code
        self.message = message
        super().__init__(self.message)
