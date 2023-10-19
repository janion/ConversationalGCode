from math import ceil, tan, pi, isclose, pow

from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.gcodes.GCodes import Comment, G0, G1
from conversational_gcode.Jsonable import Jsonable


class RectangularProfile(Jsonable):

    def __init__(self,
                 width: float = 10,
                 length: float = 10,
                 depth: float = 3,
                 centre: list = None,
                 corner: list = None,
                 start_depth: float = 0,
                 is_inner: bool = True):
        self._width = width
        self._length = length
        self._depth = depth

        if centre is not None:
            self._centre = centre
        if corner is not None:
            self._corner = corner
        if centre is None and corner is None:
            self._centre = [0, 0]
        
        self._start_depth = start_depth
        self._is_inner = is_inner

    def validate(self, options=None):
        results = []
        if self._width is None or self._width <= 0:
            results.append(ValidationResult(False, 'Profile width must be positive and non-zero'))
        if self._length is None or self._length <= 0:
            results.append(ValidationResult(False, 'Profile length must be positive and non-zero'))
        if self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Profile depth must be positive and non-zero'))
        if self._centre is None and self._corner is None:
            results.append(ValidationResult(False, 'Profile corner or centre coordinates must be specified'))
        if self._centre is not None and self._corner is not None:
            results.append(ValidationResult(False, 'Profile corner or centre coordinates must be specified, not both'))
        if self._is_inner is None:
            results.append(ValidationResult(False, 'Profile must be specified as either inner or outer (True = inner, False = outer)'))

        if options is not None:
            if self._is_inner and (self._width <= options.tool.tool_diameter or self._length <= options.tool.tool_diameter):
                results.append(ValidationResult(False, f'Profile size [{self._width}, {self._length}]mm must be greater than tool diameter {options.tool.tool_diameter}mm'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_width(self, value):
        self._width = value

    def _set_length(self, value):
        self._length = value

    def _set_depth(self, value):
        self._depth = value

    def _set_centre(self, value):
        self._centre = value

    def _set_corner(self, value):
        self._corner = value

    def _set_start_depth(self, value):
        self._start_depth = value

    def _set_is_inner(self, value):
        self._is_inner = value

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

    def generate(self, position, commands, options):
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

        if self._is_inner:
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
                commands.append(G1(x=position[0], y=position[1], z=position[2], f=tool_options.finishing_feed_rate))

        commands.append(Comment('Final pass at full depth'))
        for travel in travels:
            position[0] += travel[0]
            position[1] += travel[1]
            commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
