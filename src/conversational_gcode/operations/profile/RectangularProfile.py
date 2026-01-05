"""
Operation to create a rectangular profile.

Classes:
- RectangularProfile
  - Operation to create a rectangular profile.
"""

from math import ceil, tan, pi, isclose

from conversational_gcode.operations.Operation import Operation
from conversational_gcode.options.Options import Options
from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.gcodes.GCodes import GCode, G0, G1


class RectangularProfile(Operation):
    """
    Operation to create a rectangular profile.

    The profile is created by traversing the profile outline in the XY-plane, while also slowly plunging in the Z-axis.
    Once the tool has reached the final depth, the profile will be traversed once more to cut the entire profile at
    full depth.
    """

    def __init__(self,
                 width: float = 10,
                 length: float = 10,
                 depth: float = 3,
                 centre: list = None,
                 corner: list = None,
                 start_depth: float = 0,
                 is_inner: bool = True,
                 is_climb: bool = False):
        """
        Initialise the profile operation.
        :param width: X-axis size of the profile centre. Defaults to 10mm.
        :param length: Y-axis of the profile centre. Defaults to 10mm.
        :param depth: The depth of the profile below the start depth. Defaults to 3mm.
        :param centre: [X, Y] location of the profile centre. Defaults to [0, 0] if centre and corner not set.
        :param corner: [X, Y] location of the minimum X and Y corner of the profile,
            bottom left if X axis is left to right, and Y axis is near to far. Defaults to None.
        :param start_depth: The Z axis depth at which the profile starts. Defaults to 0mm.
        :param is_inner: True if this operation is to cut an inside profile, False if to cut an outside profile.
            Defaults to True.
        :param is_climb: True if this operation is to climb cut the profile, False if to cut conventionally. Defaults
            to False.
        """
        self._width = width
        self._length = length
        self._depth = depth

        self._centre = centre
        self._corner = corner
        if centre is None and corner is None:
            self._centre = [0, 0]

        self._start_depth = start_depth
        self._is_inner = is_inner
        self._is_climb = is_climb

    def validate(self, options=None):
        results = []
        if self._width is None or self._width <= 0:
            results.append(ValidationResult(False, 'Profile width must be positive and non-zero'))
        if self._length is None or self._length <= 0:
            results.append(ValidationResult(False, 'Profile length must be positive and non-zero'))
        if self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Profile depth must be positive and non-zero'))
        if self._start_depth is None:
            results.append(ValidationResult(False, 'Profile start depth must be specified'))
        if self._centre is None and self._corner is None:
            results.append(ValidationResult(False, 'Profile corner or centre coordinates must be specified'))
        if self._centre is not None and self._corner is not None:
            results.append(ValidationResult(False, 'Profile corner or centre coordinates must be specified, not both'))
        if self._is_inner is None:
            results.append(ValidationResult(False, 'Profile must be specified as either inner or outer (True = inner, False = outer)'))
        if self._is_climb is None:
            results.append(ValidationResult(False, 'Profile must be specified as either climb or not (True = climb, False = conventional)'))

        if options is not None:
            if self._is_inner and (self._width <= options.tool.tool_diameter or self._length <= options.tool.tool_diameter):
                results.append(ValidationResult(False, f'Profile size [{self._width}, {self._length}]mm must be greater than tool diameter {options.tool.tool_diameter}mm'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_width(self, value: float) -> None:
        self._width = value

    def _set_length(self, value: float) -> None:
        self._length = value

    def _set_depth(self, value: float) -> None:
        self._depth = value

    def _set_centre(self, value: list[float]) -> None:
        self._centre = value

    def _set_corner(self, value: list[float]) -> None:
        self._corner = value

    def _set_start_depth(self, value: float) -> None:
        self._start_depth = value

    def _set_is_inner(self, value: bool) -> None:
        self._is_inner = value

    def _set_is_climb(self, value: bool) -> None:
        self._is_climb = value

    width = property(
        fget=lambda self: self._width,
        fset=_set_width
    )
    length = property(
        fget=lambda self: self._length,
        fset=_set_length
    )
    depth = property(
        fget=lambda self: self._depth,
        fset=_set_depth
    )
    centre = property(
        fget=lambda self: self._centre,
        fset=_set_centre
    )
    corner = property(
        fget=lambda self: self._corner,
        fset=_set_corner
    )
    start_depth = property(
        fget=lambda self: self._start_depth,
        fset=_set_start_depth
    )
    is_inner = property(
        fget=lambda self: self._is_inner,
        fset=_set_is_inner
    )
    is_climb = property(
        fget=lambda self: self._is_climb,
        fset=_set_is_climb
    )

    def generate(self, position: list[float], commands: list[GCode], options: Options) -> None:
        # Setup
        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        if self._is_inner:
            pocket_final_size = [self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter]
        else:
            pocket_final_size = [self._width + tool_options.tool_diameter, self._length + tool_options.tool_diameter]

        total_plunge = job_options.lead_in + self._depth
        total_xy_travel = sum(pocket_final_size) * 2

        max_plunge_per_step_using_angle = total_xy_travel * tan(tool_options.max_helix_angle * pi / 180)
        plunge_per_step_using_angle = total_plunge / ceil(total_plunge / max_plunge_per_step_using_angle)

        max_plunge_per_step = min(tool_options.max_stepdown, plunge_per_step_using_angle)
        step_plunge = total_plunge / ceil(total_plunge / max_plunge_per_step)

        if self._centre is not None:
            centre = self._centre
        else:
            centre = [self._corner[0] + self._width / 2, self._corner[1] + self._length / 2]

        # Position tool
        position[0] = centre[0] + pocket_final_size[0] / 2
        position[1] = centre[1] + pocket_final_size[1] / 2
        commands.append(G0(x=position[0], y=position[1], comment='Move to starting position'))
        position[2] = self._start_depth + job_options.lead_in
        commands.append(G0(z=position[2], comment='Move to start depth'))

        x_travel_plunge = step_plunge * pocket_final_size[0] / total_xy_travel
        y_travel_plunge = step_plunge * pocket_final_size[1] / total_xy_travel

        if self._is_inner != self._is_climb:
            travels = [
                [0, -pocket_final_size[1], -y_travel_plunge],
                [-pocket_final_size[0], 0, -x_travel_plunge],
                [0, pocket_final_size[1], -y_travel_plunge],
                [pocket_final_size[0], 0, -x_travel_plunge]
            ]
        else:
            travels = [
                [-pocket_final_size[0], 0, -x_travel_plunge],
                [0, -pocket_final_size[1], -y_travel_plunge],
                [pocket_final_size[0], 0, -x_travel_plunge],
                [0, pocket_final_size[1], -y_travel_plunge]
            ]

        while not isclose(position[2], self._start_depth - self._depth, abs_tol=pow(10, -precision)):
            for travel in travels:
                position[0] += travel[0]
                position[1] += travel[1]
                position[2] += travel[2]
                commands.append(G1(x=position[0], y=position[1], z=position[2], f=tool_options.feed_rate))

        commands.append(GCode('Final pass at full depth'))
        for travel in travels:
            position[0] += travel[0]
            position[1] += travel[1]
            commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

    def to_json(self) -> str:
        return (
                '{' +
                f'"width":{self._width},' +
                f'"length":{self._length},' +
                f'"depth":{self._depth},' +
                f'"centre":[{self._centre[0]},{self._centre[1]}],' +
                f'"corner":[{self._corner[0]},{self._corner[1]}],' +
                f'"start_depth":{self._start_depth},' +
                f'"is_inner":{str(self._is_inner).lower()},' +
                f'"is_climb":{str(self._is_climb).lower()},' +
                '}'
        ).replace(',}', '}')

    def __repr__(self) -> str:
        return (
            'RectangularProfile(' +
            f'width={self.width}, length={self.length}, ' +
            f'centre={self.centre}, corner={self.corner}, ' +
            f'depth={self.depth}, start_depth={self.start_depth}, ' +
            f'is_inner={self.is_inner}, is_climb={self.is_climb}' +
            ')'
        )
