class ValidationResult:

    def __init__(self, success: bool = True, message: str = None):
        self._success = success
        self._message = message
        if self._message is None:
            self._message = 'Valid' if success else "Invalid"

    success = property(fget=lambda self: self._success)
    message = property(fget=lambda self: self._message)
