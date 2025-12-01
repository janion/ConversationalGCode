"""
Result of validating a configuration.

Classes:
- ValidationResult
  - Contains validation status and message.
"""


class ValidationResult:
    """
    Contains validation status and message.

    Attributes:
        success (bool): True if the result is valid
        message (str): Message for the user. Defaults to None to set the message to either
                 "Valid" or "Invalid", depending on the success status.
    """

    def __init__(self, success: bool = True, message: str = None):
        """
        Initialise the validation result.
        :param success: True if the object is valid. Defaults to True.
        :param message: Message to explain the status. Defaults to None to set the message to either
                 "Valid" or "Invalid", depending on the success status.
        """
        self._success = success
        self._message = message
        if self._message is None:
            self._message = 'Valid' if success else "Invalid"

    success = property(fget=lambda self: self._success)
    message = property(fget=lambda self: self._message)

    def __repr__(self):
        return f'ValidationResult(success={self._success}, message={self._message})'
