from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.operations.Operations import helical_plunge
from conversational_gcode.gcodes.GCodes import Comment, G0


class CircularProfile:

    def __init__(self,
                 centre: list = None,
                 start_depth: float = 0,
                 diameter: float = 10,
                 depth: float = 3,
                 is_inner: bool = True):
        self._centre = [0, 0] if centre is None else centre
        self._start_depth = start_depth
        self._diameter = diameter
        self._depth = depth
        self._is_inner = is_inner

    def validate(self, options = None):
        results = []
        if self._centre is None:
            results.append(ValidationResult(False, 'Profile centre coordinates must be specified'))
        elif self._start_depth is None:
            results.append(ValidationResult(False, 'Profile start depth must be specified'))
        elif self._diameter is None or self._diameter <= 0:
            results.append(ValidationResult(False, 'Profile diameter must be positive and non-zero'))
        elif self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Profile depth must be positive and non-zero'))
        elif self._is_inner is None:
            results.append(ValidationResult(False, 'Profile must be specified as either inner or outer (True = inner, False = outer)'))

        if options is not None:
            if self._is_inner and self._diameter <= options.tool.tool_diameter:
                results.append(ValidationResult(False, f'Inner profile diameter {self._diameter}mm must be greater than tool diameter {options.tool.tool_diameter}mm'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_centre(self, value):
        self._centre = value

    def _set_start_depth(self, value):
        self._start_depth = value

    def _set_diameter(self, value):
        self._diameter = value

    def _set_depth(self, value):
        self._depth = value

    def _set_is_inner(self, value):
        self._is_inner = value

    centre = property(
        fget=lambda self: self._centre,
        fset=_set_centre
    )
    start_depth = property(
        fget=lambda self: self._start_depth,
        fset=_set_start_depth
    )
    diameter = property(
        fget=lambda self: self._diameter,
        fset=_set_diameter
    )
    depth = property(
        fget=lambda self: self._depth,
        fset=_set_depth
    )
    is_inner = property(
        fget=lambda self: self._is_inner,
        fset=_set_is_inner
    )

    def generate(self, position, commands, options):
        # Setup
        tool_options = options.tool
        job_options = options.job

        commands.append(Comment('Circular profile'))

        if self._is_inner:
            path_radius = (self._diameter - tool_options.tool_diameter) / 2
        else:
            path_radius = (self._diameter + tool_options.tool_diameter) / 2

        # Position tool ready to begin
        self._move_to_centre(position, commands, job_options)

        helical_plunge(self._centre, path_radius, job_options.lead_in + self._depth, position, commands, tool_options, options.output.position_precision)

    def _move_to_centre(self, position, commands, job_options):
        # Position tool at hole centre
        position[0] = self._centre[0]
        position[1] = self._centre[1]
        commands.append(G0(x=position[0], y=position[1], comment='Move to hole position'))
        position[2] = self._start_depth + job_options.lead_in
        commands.append(G0(z=position[2], comment='Move to hole start depth'))
