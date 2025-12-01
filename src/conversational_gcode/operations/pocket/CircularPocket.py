"""
Operation to create a circular pocket.

Classes:
- CircularPocket
  - Operation to create a circular pocket.
"""

from math import ceil, isclose

from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.operations.Operations import helical_plunge, spiral_out
from conversational_gcode.gcodes.GCodes import GCode, G0, G2, G3


class CircularPocket:
    """
    Operation to create a circular pocket.

    The pocket is created by helically interpolating at the pocket centre, then spiralling out to the final diameter.
    This is done in multiple, evenly sized steps based on the configured stepdown.
    """

    def __init__(self,
                 centre: list[float] = None,
                 start_depth: float = 0,
                 diameter: float = 10,
                 depth: float = 10,
                 finishing_pass: bool = False):
        """
        Initialise the pocket operation.
        :param centre: [X, Y] location of the pocket centre. Defaults to [0, 0].
        :param start_depth: The Z-axis depth at which the pocket starts. Defaults to 0mm.
        :param diameter: The diameter of the pocket. Defaults to 10mm.
        :param depth: The depth of the pocket below the start depth. Defaults to 10mm.
        :param finishing_pass: True if this operation includes a finishing pass. Defaults to False to indicate no
            finishing pass.
        """
        self._centre = [0, 0] if centre is None else centre
        self._start_depth = start_depth
        self._diameter = diameter
        self._depth = depth
        self._finishing_pass = finishing_pass

    def validate(self, options=None):
        results = []
        if self._centre is None:
            results.append(ValidationResult(False, 'Pocket centre coordinates must be specified'))
        if self._start_depth is None:
            results.append(ValidationResult(False, 'Pocket start depth must be specified'))
        if self._diameter is None or self._diameter <= 0:
            results.append(ValidationResult(False, 'Pocket diameter must be positive and non-zero'))
        if self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Pocket depth must be positive and non-zero'))

        if options is not None:
            if self._diameter <= options.tool.tool_diameter:
                results.append(ValidationResult(False, f'Hole diameter {self._diameter}mm must be greater than tool diameter {options.tool.tool_diameter}mm'))

            roughing_diameter = self._diameter
            has_finishing_pass = self._finishing_pass and options.tool.finishing_pass > 0
            if has_finishing_pass and roughing_diameter <= options.tool.tool_diameter:
                results.append(ValidationResult(False, f'Hole diameter {self._diameter}mm must be greater than tool diameter {options.tool.tool_diameter}mm and give room for a finishing pass of {options.tool.finishing_pass}mm'))

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

    def _set_finishing_pass(self, value):
        self._finishing_pass = value

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
    finishing_pass = property(
        fget=lambda self: self._finishing_pass is not None and self._finishing_pass,
        fset=_set_finishing_pass
    )

    def generate(self, position, commands, options):
        #########
        # Setup #
        #########
        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        roughing_diameter = self._diameter
        has_finishing_pass = self._finishing_pass and tool_options.finishing_pass > 0

        if has_finishing_pass:
            roughing_diameter -= 2 * tool_options.finishing_pass

        final_path_radius = (roughing_diameter - tool_options.tool_diameter) / 2
        initial_path_radius = min(final_path_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_centre(position, commands, job_options)

        total_plunge = job_options.lead_in + self._depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        if final_path_radius <= tool_options.max_helix_stepover:
            # Helical interpolate to final depth as there is no need to spiral out to final diameter
            helical_plunge(self._centre, initial_path_radius, total_plunge, position,
                           commands, tool_options, precision)
        else:
            # Mill out material in depth steps
            final_depth = self._start_depth - self._depth
            deepest_cut_depth = position[2]
            while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                path_radius = initial_path_radius
                position[2] = deepest_cut_depth

                # Helical interpolate to depth
                helical_plunge(self._centre, path_radius, step_plunge, position,
                               commands, tool_options, precision)

                deepest_cut_depth = position[2]
                if not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
                    # Spiral out to final radius
                    spiral_out(path_radius, final_path_radius, position, commands, tool_options, precision)

                    # Return to centre
                    if not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                        self._clear_wall(position, commands, job_options)
                    commands.append(GCode())

        # Finishing pass
        if has_finishing_pass:
            self._create_finishing_pass(position, commands, tool_options, precision)
        # Clear wall
        self._clear_wall(position, commands, job_options)

    def _move_to_centre(self, position, commands, job_options):
        # Position tool at hole centre
        position[0] = self._centre[0]
        position[1] = self._centre[1]
        commands.append(G0(x=position[0], y=position[1], comment='Move to hole position'))
        position[2] = self._start_depth + job_options.lead_in
        commands.append(G0(z=position[2], comment='Move to hole start depth'))

    def _clear_wall(self, position, commands, job_options):
        if position[0] > self._centre[0]:
            position[0] = max(position[0] - 1, self._centre[0])
        else:
            position[0] = min(position[0] + 1, self._centre[0])

        position[2] += job_options.lead_in
        commands.append(G0(x=position[0], z=position[2], comment='Move cutter away from wall'))

    def _create_finishing_pass(self, position, commands, tool_options, precision):
        commands.append(GCode(f'Finishing pass of {tool_options.finishing_pass:.{precision}f}mm'))

        is_right = position[0] > self._centre[0]

        if is_right:
            path_radius = position[0] - self._centre[0]
            relative_centre_multiplier = -1
        else:
            path_radius = self._centre[0] - position[0]
            relative_centre_multiplier = 1

        # Spiral out to finishing depth over half turn
        position[0] += (path_radius * 2 + tool_options.finishing_pass) * relative_centre_multiplier
        relative_centre = (path_radius + tool_options.finishing_pass / 2) * relative_centre_multiplier

        if tool_options.finishing_climb:
            finishing_command = G3
        else:
            finishing_command = G2

        commands.append(
            finishing_command(x=position[0], y=position[1], i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Spiral out to finishing pass'))
        # Full circle at finishing depth
        relative_centre = -(path_radius + tool_options.finishing_pass) * relative_centre_multiplier
        commands.append(
            finishing_command(x=position[0], y=position[1], i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Complete circle at final radius'))

    def to_json(self):
        return (
                '{' +
                f'"centre":[{self._centre[0]},{self._centre[1]}],' +
                f'"start_depth":{self._start_depth},' +
                f'"diameter":{self._diameter},' +
                f'"depth":{self._depth},' +
                f'"finishing_pass":{str(self._finishing_pass).lower()},' +
                '}'
        ).replace(',}', '}')

    def __repr__(self):
        return (
            'CircularPocket(' +
            f'diameter={self.diameter}, centre={self.centre}, ' +
            f'depth={self.depth}, start_depth={self.start_depth}, ' +
            f'finishing_pass={self.finishing_pass}' +
            ')'
        )
