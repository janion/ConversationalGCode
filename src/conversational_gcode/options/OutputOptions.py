from conversational_gcode.validate.validation_result import ValidationResult


class OutputOptions:

    def __init__(self, position_precision: int = 3, feed_precision: int = 2, speed_precision: int = 1):
        self._position_precision = position_precision
        self._feed_precision = feed_precision
        self._speed_precision = speed_precision

    def validate(self):
        results = []
        if self._position_precision is None or self._position_precision < 0:
            results.append(ValidationResult(False, 'Position precision must be zero or greater'))
        if self._feed_precision is None or self._feed_precision < 0:
            results.append(ValidationResult(False, 'Feed precision must be zero or greater'))
        if self._speed_precision is None or self._speed_precision < 0:
            results.append(ValidationResult(False, 'Speed precision must be zero or greater'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_position_precision(self, value):
        self._position_precision = value

    def _set_feed_precision(self, value):
        self._feed_precision = value

    def _set_speed_precision(self, value):
        self._speed_precision = value

    position_precision = property(
        fget=lambda self: self._position_precision,
        fset=_set_position_precision
    )
    feed_precision = property(
        fget=lambda self: self._feed_precision,
        fset=_set_feed_precision
    )
    speed_precision = property(
        fget=lambda self: self._speed_precision,
        fset=_set_speed_precision
    )
