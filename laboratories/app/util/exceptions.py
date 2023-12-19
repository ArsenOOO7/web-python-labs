class AccessTokenException(Exception):
    """ Raised when something wrong with JWT Token """

    def __init__(self, message, response_code: int = 401):
        self.response_code = response_code
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(Exception):
    """ Raised when entity not found """

    def __init(self, entity_name: str, id: int):
        self.entity_name = entity_name
        self.message = f"Entity {{entity_name}} with id {id} is not found"
        super().__init__(self.message)