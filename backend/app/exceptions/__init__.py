
class UnprocessableEntityException(Exception):
    def __init__(self, message: str = "Unprocessable Entity Exception"):
        code = 422
        super().__init__(code, message)
