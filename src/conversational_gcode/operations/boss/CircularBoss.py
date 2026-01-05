"""
Operation to create a circular boss.

Classes:
- CircularBoss
  - Operation to create a circular boss.
"""

from math import ceil, isclose
from typing import Tuple

from conversational_gcode.operations.Operation import Operation
from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.Options import Options
from conversational_gcode.options.ToolOptions import ToolOptions
from conversational_gcode.position.Position import Position
from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.operations.Operations import helical_plunge, spiral_in
from conversational_gcode.gcodes.GCodes import GCode, G0, G2, G3


class CircularBoss(Operation):
    """
    Operation to create a circular boss.

    The boss is created by helically interpolating at the start diameter, then spiralling in to the final diameter.
    This is done in multiple, evenly sized steps based on the configured stepdown.
    """

    def __init__(self,
                 centre: Tuple[float, float] = None,
                 top_height: float = 0,
                 initial_diameter: float = 20,
                 final_diameter: float = 10,
                 height: float = 10,
                 finishing_pass: bool = False):
        """
        Initialise the boss operation.
        :param centre: (X, Y) location of the boss centre. Defaults to (0, 0).
        :param top_height: The Z-axis height at which the boss starts. Defaults to 0mm.
        :param initial_diameter: The diameter at which to start  cutting the boss. Defaults to 20mm.
        :param final_diameter: The diameter of the boss. Defaults to 10mm.
        :param height: The height of the boss below the start height. Defaults to 10mm.
        :param finishing_pass: True if this operation includes a finishing pass. Defaults to False to indicate no
            finishing pass.
        """
        self._centre = (0, 0) if centre is None else centre
        self._top_height = top_height
        self._initial_diameter = initial_diameter
        self._final_diameter = final_diameter
        self._height = height
        self._finishing_pass = finishing_pass

    def validate(self, options: Options = None) -> list[ValidationResult]:
        results = []
        if self._centre is None:
            results.append(ValidationResult(False, 'Boss centre coordinates must be specified'))
        if self._top_height is None:
            results.append(ValidationResult(False, 'Boss start height must be specified'))
        if self._final_diameter is None or self._final_diameter <= 0:
            results.append(ValidationResult(False, 'Boss final diameter must be positive and non-zero'))
        elif self._initial_diameter is None or self._initial_diameter <= self._final_diameter:
            results.append(ValidationResult(False, 'Boss initial diameter must be greater than the final diameter'))
        if self._height is None or self._height <= 0:
            results.append(ValidationResult(False, 'Boss height must be positive and non-zero'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_centre(self, value: Tuple[float, float]) -> None:
        self._centre = (0, 0) if value is None else value

    def _set_top_height(self, value: float) -> None:
        self._top_height = value

    def _set_initial_diameter(self, value: float) -> None:
        self._initial_diameter = value

    def _set_final_diameter(self, value: float) -> None:
        self._final_diameter = value

    def _set_height(self, value: float) -> None:
        self._height = value

    def _set_finishing_pass(self, value: bool) -> None:
        self._finishing_pass = value

    centre = property(
        fget=lambda self: self._centre,
        fset=_set_centre
    )
    top_height = property(
        fget=lambda self: self._top_height,
        fset=_set_top_height
    )
    initial_diameter = property(
        fget=lambda self: self._initial_diameter,
        fset=_set_initial_diameter
    )
    final_diameter = property(
        fget=lambda self: self._final_diameter,
        fset=_set_final_diameter
    )
    height = property(
        fget=lambda self: self._height,
        fset=_set_height
    )
    finishing_pass = property(
        fget=lambda self: self._finishing_pass is not None and self._finishing_pass,
        fset=_set_finishing_pass
    )

    def generate(self, position: Position, commands: list[GCode], options: Options) -> None:
        #########
        # Setup #
        #########
        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        roughing_diameter = self._final_diameter
        has_finishing_pass = self._finishing_pass and tool_options.finishing_pass > 0

        if has_finishing_pass:
            roughing_diameter += 2 * tool_options.finishing_pass

        final_path_radius = (roughing_diameter + tool_options.tool_diameter) / 2

        # Position tool ready to begin
        self._move_to_centre(position, commands, job_options)

        total_plunge = job_options.lead_in + self._height
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        # Mill away material in depth steps
        final_depth = self._top_height - self._height
        deepest_cut_depth = position.z
        while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
            initial_path_radius = (self._initial_diameter + tool_options.tool_diameter) / 2
            position.z = deepest_cut_depth

            # Helical interpolate to depth
            helical_plunge(self._centre, initial_path_radius, step_plunge, position,
                           commands, tool_options, precision, is_inner=False)

            deepest_cut_depth = position.z
            if not isclose(initial_path_radius, final_path_radius, abs_tol=pow(10, -precision)):
                # Spiral in to final radius
                spiral_in(initial_path_radius, final_path_radius, position, commands, tool_options, precision)

                if not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                    self._clear_wall(position, commands, job_options)
                    position.z = job_options.clearance_height
                    commands.append(G0(z=position.z))
                    position.x = self._centre[0] + initial_path_radius
                    commands.append(G0(x=position.x))
                commands.append(GCode())

        # Finishing pass
        if has_finishing_pass:
            self._create_finishing_pass(position, commands, tool_options, precision)
        # Clear wall
        self._clear_wall(position, commands, job_options)

    def _move_to_centre(self, position: Position, commands: list[GCode], job_options: JobOptions) -> None:
        # Position tool at hole centre
        position.x = self._centre[0]
        position.y = self._centre[1]
        commands.append(G0(x=position.x, y=position.y, comment='Move to hole position'))
        position.z = self._top_height + job_options.lead_in
        commands.append(G0(z=position.z, comment='Move to hole start height'))

    def _clear_wall(self, position: Position, commands: list[GCode], job_options: JobOptions) -> None:
        if position.x > self._centre[0]:
            position.x = max(position.x + 1, self._centre[0])
        else:
            position.x = min(position.x - 1, self._centre[0])

        position.z += job_options.lead_in
        commands.append(G0(x=position.x, z=position.z, comment='Move cutter away from wall'))

    def _create_finishing_pass(self, position: Position, commands: list[GCode], tool_options: ToolOptions, precision: int):
        commands.append(GCode(f'Finishing pass of {tool_options.finishing_pass:.{precision}f}mm'))

        is_right = position.x > self._centre[0]

        if is_right:
            path_radius = position.x - self._centre[0]
            relative_centre_multiplier = -1
        else:
            path_radius = self._centre[0] - position.x
            relative_centre_multiplier = 1

        # Spiral in to finishing depth over half turn
        position.x += (path_radius * 2 - tool_options.finishing_pass) * relative_centre_multiplier
        relative_centre = (path_radius - tool_options.finishing_pass / 2) * relative_centre_multiplier

        if tool_options.finishing_climb:
            finishing_command = G3
        else:
            finishing_command = G2

        commands.append(
            finishing_command(x=position.x, y=position.y, i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Spiral out to finishing pass'))
        # Full circle at finishing depth
        relative_centre = -(path_radius - tool_options.finishing_pass) * relative_centre_multiplier
        commands.append(
            finishing_command(x=position.x, y=position.y, i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Complete circle at final radius'))

    def to_json(self) -> str:
        return (
                '{' +
                f'"centre":[{self._centre[0]},{self._centre[1]}],' +
                f'"top_height":{self._top_height},' +
                f'"initial_diameter":{self._initial_diameter},' +
                f'"final_diameter":{self._final_diameter},' +
                f'"height":{self._height},' +
                f'"finishing_pass":{str(self._finishing_pass).lower()},' +
                '}'
        ).replace(',}', '}')

    def __repr__(self) -> str:
        return (
            'CircularBoss(' +
            f'centre={self.centre}, ' +
            f'initial_diameter={self.initial_diameter}, final_diameter={self.final_diameter}, ' +
            f'height={self.height}, top_height={self.top_height}, ' +
            f'finishing_pass={self.finishing_pass}' +
            ')'
        )
