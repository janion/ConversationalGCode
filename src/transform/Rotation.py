from dataclasses import dataclass


@dataclass
class Rotation:
    absolute: list
    relative: list

    def transform_absolute(self, point):
        new_x = self.absolute[0](*point)
        new_y = self.absolute[1](*point)
        new_z = self.absolute[2](*point)
        return [new_x, new_y, new_z]

    def transform_relative(self, point):
        new_x = self.relative[0](*point)
        new_y = self.relative[1](*point)
        new_z = self.relative[2](*point)
        return [new_x, new_y, new_z]
