"""
Transforms points in space.

Classes:
- Transformation
  - Represents a single transformation of a point in space.
"""

from dataclasses import dataclass


@dataclass
class Transformation:
    """
    Represents a single transformation of a point in space.

    Attributes:
        absolute (list): 3 functions to apply to the [X, Y, Z] coordinates of absolute points.
        relative (list): 3 functions to apply to the [X, Y, Z] coordinates of relative points.
    """

    absolute: list
    relative: list

    def transform_absolute(self, point):
        """
        Transform an absolute point.
        :param point: [X, Y, Z] position to transform.
        :return: Transformed copy of original point.
        """
        new_x = self.absolute[0](*point)
        new_y = self.absolute[1](*point)
        new_z = self.absolute[2](*point)
        return [new_x, new_y, new_z]

    def transform_relative(self, point):
        """
        Transform a relative point.
        :param point: [X, Y, Z] position to transform.
        :return: Transformed copy of original point.
        """
        new_x = self.relative[0](*point)
        new_y = self.relative[1](*point)
        new_z = self.relative[2](*point)
        return [new_x, new_y, new_z]
