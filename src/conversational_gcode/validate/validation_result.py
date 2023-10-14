class ValidationResult:

    def __init__(self, success: bool = True, message: str = ''):
        self._success = success
        self._message = message

    success = property(fget=lambda self: self._success)
    message = property(fget=lambda self: self._message)
