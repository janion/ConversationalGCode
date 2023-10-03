
class OutputOptions:

    def __init__(self, position_precision: int = 3, feed_precision: int = 2, speed_precision: int = 1):
        if position_precision < 0:
            raise ValueError('Position precision must be zero or greater')
        elif feed_precision < 0:
            raise ValueError('Feed precision must be zero or greater')
        elif speed_precision < 0:
            raise ValueError('Speed precision must be zero or greater')

        self._position_precision = position_precision
        self._feed_precision = feed_precision
        self._speed_precision = speed_precision

    position_precision = property(
        fget=lambda self: self._position_precision
    )

    feed_precision = property(
        fget=lambda self: self._feed_precision
    )

    speed_precision = property(
        fget=lambda self: self._speed_precision
    )
