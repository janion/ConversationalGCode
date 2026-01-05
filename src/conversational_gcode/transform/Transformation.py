"""
Transforms points in space.

Classes:
- Transformation
  - Represents a single transformation of a point in space.
"""

from dataclasses import dataclass
from typing import Callable, Tuple

from conversational_gcode.position.Position import Position


@dataclass
class Transformation:
    """
    Represents a single transformation of a point in space.

    Attributes:
        absolute: 3 functions to apply to the (X, Y, Z) coordinates of absolute points.
        relative: 3 functions to apply to the (X, Y, Z) coordinates of relative points.
    """

    absolute: Tuple[Callable[[Position], float], Callable[[Position], float], Callable[[Position], float]]
    relative: Tuple[Callable[[Position], float], Callable[[Position], float], Callable[[Position], float]]

    def transform_absolute(self, point: Position) -> Position:
        """
        Transform an absolute point.
        :param point: (X, Y, Z) position to transform.
        :return: Transformed copy of original point.
        """
        new_x = self.absolute[0](point)
        new_y = self.absolute[1](point)
        new_z = self.absolute[2](point)
        return Position(new_x, new_y, new_z)

    def transform_relative(self, point: Position) -> Position:
        """
        Transform a relative point.
        :param point: (X, Y, Z) position to transform.
        :return: Transformed copy of original point.
        """
        new_x = self.relative[0](point)
        new_y = self.relative[1](point)
        new_z = self.relative[2](point)
        return Position(new_x, new_y, new_z)

    def __repr__(self) -> str:
        return (
            'Transformation(' +
            f'absolute={self.absolute!r}, ' +
            f'relative={self.relative!r}' +
            ')'
        )
