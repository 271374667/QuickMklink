class ExceptionTagError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ExceptionTagError: {self.message}"


class ExceptionTagNoFoundError(ExceptionTagError):
    def __str__(self):
        return f"ExceptionTagNoFoundError: {self.message}"
