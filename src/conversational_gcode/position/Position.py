class Position:
    """
    Cartesian coordinates of a position.
    """

    def __init__(self,
                 x: float = None,
                 y: float = None,
                 z: float = None):
        """
        Initialise the position.
        :param x: X coordinate of position. Defaults to None
        :param y: Y coordinate of position. Defaults to None
        :param z: Z coordinate of position. Defaults to None
        """
        self._x = x
        self._y = y
        self._z = z

    def _set_x(self, value: float) -> None:
        if value is None:
            raise ValueError('Cannot set X position to None')
        self._x = value

    def _set_y(self, value: float) -> None:
        if value is None:
            raise ValueError('Cannot set Y position to None')
        self._y = value

    def _set_z(self, value: float) -> None:
        if value is None:
            raise ValueError('Cannot set Z position to None')
        self._z = value

    x = property(
        fget=lambda self: self._x,
        fset=_set_x
    )

    y = property(
        fget=lambda self: self._y,
        fset=_set_y
    )

    z = property(
        fget=lambda self: self._z,
        fset=_set_z
    )

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Position):
            return False
        return self._x == __o._x and self._y == __o._y and self._z == __o._z
