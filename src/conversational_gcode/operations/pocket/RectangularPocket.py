"""
Operation to create a rectangular pocket.

Classes:
- RectangularPocket
  - Operation to create a rectangular pocket.
"""

from math import ceil,  isclose, sqrt
from copy import deepcopy
from typing import Tuple, Callable

from conversational_gcode.operations.Operation import Operation
from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.Options import Options
from conversational_gcode.position.Position import Position
from conversational_gcode.validate.validation_result import ValidationResult
from conversational_gcode.operations.Operations import rapid_with_z_hop, helical_plunge, spiral_out
from conversational_gcode.gcodes.GCodes import GCode, G0, G1, G2
from conversational_gcode.transform.Transformation import Transformation


class RectangularPocket(Operation):
    """
    Operation to create a rectangular pocket.

    The pocket is created by helically interpolating at one end of the pocket, then spiralling out to the final width,
    then clearing the near corners, followed by the far corners, using arcs centred at the original plunge location.
    This is done in multiple, evenly sized steps based on the configured stepdown.
    """

    def __init__(self,
                 width: float = 10,
                 length: float = 10,
                 depth: float = 3,
                 centre: Tuple[float, float] = None,
                 corner: Tuple[float, float] = None,
                 start_depth: float = 0,
                 finishing_pass: bool = False):
        """
        Initialise the pocket operation.
        :param width: X-axis size of the pocket centre. Defaults to 10mm.
        :param length: Y-axis of the pocket centre. Defaults to 10mm.
        :param depth: The depth of the pocket below the start depth. Defaults to 3mm.
        :param centre: (X, Y) location of the pocket centre. Defaults to (0, 0) if centre and corner not set.
        :param corner: (X, Y) location of the minimum X and Y corner of the pocket,
            bottom left if X axis is left to right, and Y axis is near to far. Defaults to None.
        :param start_depth: The Z axis depth at which the pocket starts. Defaults to 0mm.
        :param finishing_pass: True if this operation includes a finishing pass. Defaults to False to indicate no
            finishing pass.
        """
        self._width = width
        self._length = length
        self._depth = depth

        self._centre = centre
        self._corner = corner
        if centre is None and corner is None:
            self._centre = (0, 0)
        
        self._start_depth = start_depth
        self._finishing_pass = finishing_pass

    def validate(self, options=None):
        results = []
        if self._width is None or self._width <= 0:
            results.append(ValidationResult(False, 'Pocket width must be positive and non-zero'))
        if self._length is None or self._length <= 0:
            results.append(ValidationResult(False, 'Pocket length must be positive and non-zero'))
        if self._depth is None or self._depth <= 0:
            results.append(ValidationResult(False, 'Pocket depth must be positive and non-zero'))
        if self._centre is None and self._corner is None:
            results.append(ValidationResult(False, 'Pocket corner or centre coordinates must be specified'))
        if self._centre is not None and self._corner is not None:
            results.append(ValidationResult(False, 'Pocket corner or centre coordinates must be specified, not both'))
        if self._start_depth is None:
            results.append(ValidationResult(False, 'Pocket start depth must be specified'))

        if options is not None:
            has_finishing_pass = self._finishing_pass and options.tool.finishing_pass > 0
            pocket_clearing_size = [self._width - options.tool.tool_diameter, self._length - options.tool.tool_diameter]

            if self._width is None or self._length is None or self._depth is None:
                results.append(ValidationResult(False, 'Rectangular pocket must have width, length and depth defined.'))
            if self._width <= options.tool.tool_diameter or self._length <= options.tool.tool_diameter:
                results.append(ValidationResult(False, f'Pocket size [{self._width}, {self._length}]mm must be greater than tool diameter {options.tool.tool_diameter}mm'))
            if has_finishing_pass and pocket_clearing_size[0] <= 0:
                results.append(ValidationResult(False, f'Pocket size [{self._width}, {self._length}]mm must be greater than tool diameter {options.tool.tool_diameter}mm and give room for a finishing pass of {options.tool.finishing_pass}mm'))

        if len(results) == 0:
            results.append(ValidationResult())

        return results

    def _set_width(self, value: float) -> None:
        self._width = value

    def _set_length(self, value: float) -> None:
        self._length = value

    def _set_depth(self, value: float) -> None:
        self._depth = value

    def _set_centre(self, value: Tuple[float, float]) -> None:
        self._centre = value

    def _set_corner(self, value: Tuple[float, float]) -> None:
        self._corner = value

    def _set_start_depth(self, value: float) -> None:
        self._start_depth = value

    def _set_finishing_pass(self, value: bool) -> None:
        self._finishing_pass = value

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
    finishing_pass = property(
        fget=lambda self: self._finishing_pass,
        fset=_set_finishing_pass
    )

    def generate(self, position: Position, commands: list[GCode], options: Options) -> None:
        #########
        # Setup #
        #########
        operation_commands = []

        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        has_finishing_pass = self._finishing_pass and tool_options.finishing_pass > 0

        pocket_clearing_size = (self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter)
        pocket_final_size = (self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter)
        if has_finishing_pass:
            pocket_clearing_size = (
                    pocket_clearing_size[0] - 2 * tool_options.finishing_pass,
                    pocket_clearing_size[1] - 2 * tool_options.finishing_pass
            )

        if self._centre is not None:
            centre = self._centre
        else:
            centre = (self._corner[0] + self._width / 2, self._corner[1] + self._length / 2)

        rotated = False
        if self._width > self._length:
            pocket_clearing_size = (pocket_clearing_size[1], pocket_clearing_size[0])
            pocket_final_size = (pocket_final_size[1], pocket_final_size[0])
            position.x = -position.y
            position.y = position.x
            rotated = True
        pocket_clearing_centre = (centre[0], centre[1] + (pocket_clearing_size[0] - pocket_clearing_size[1]) / 2)

        final_clearing_radius = pocket_clearing_size[0] / 2
        initial_clearing_radius = min(final_clearing_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_start(Position(*pocket_clearing_centre, self._start_depth), position, operation_commands, job_options)

        total_plunge = job_options.lead_in + self._depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        ####################################
        # Mill out material in depth steps #
        ####################################
        final_depth = self._start_depth - self._depth
        deepest_cut_depth = position.z
        while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
            clearing_radius = initial_clearing_radius
            position.z = deepest_cut_depth

            operation_commands.append(GCode('Clear out circle at edge of pocket'))
            # Helical interpolate to depth
            helical_plunge(pocket_clearing_centre, clearing_radius, step_plunge, position,
                           operation_commands, tool_options, precision)

            # Spiral out to final radius
            deepest_cut_depth = position.z
            if not isclose(clearing_radius, final_clearing_radius, abs_tol=pow(10, -precision)):
                spiral_out(clearing_radius, final_clearing_radius, position, operation_commands, tool_options, precision)

            # Clear bottom corners
            corner_commands = self._clear_near_corners(pocket_clearing_centre, final_clearing_radius, position, operation_commands, options)

            # Clear arcs up to edge
            self._clear_centre(pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, position, operation_commands, options)

            # Clear far corners
            self._clear_far_corners(pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, corner_commands, position, operation_commands, options)

            if not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                # Clear wall
                self._clear_wall(centre, position, operation_commands, job_options)

        # Finishing pass
        if has_finishing_pass:
            self._create_finishing_pass(centre, pocket_final_size, position, operation_commands, options)

        # Clear wall
        self._clear_wall(centre, position, operation_commands, job_options)

        if rotated:
            position.x = position.y
            position.y = -position.x
            for command in operation_commands:
                command.transform(
                    Transformation(
                        (
                            lambda point: (point.y + centre[0] - centre[1]) if point.y is not None else None,
                            lambda point: (centre[0] + centre[1] - point.x) if point.x is not None else None,
                            lambda point: point.z if point.z is not None else None
                        ),
                        (
                            lambda point: point.y if point.y is not None else None,
                            lambda point: -point.x if point.x is not None else None,
                            lambda point: point.z if point.z is not None else None
                        )
                    )
                )

        for operation_command in operation_commands:
            commands.append(operation_command)

    def _move_to_start(self, start_position: Position, position: Position, commands: list[GCode], job_options: JobOptions) -> None:
        # Position tool at hole centre
        position.x = start_position.x
        position.y = start_position.y
        commands.append(G0(x=position.x, y=position.y, comment='Move to starting position'))
        position.z = start_position.z + job_options.lead_in
        commands.append(G0(z=position.z, comment='Move to hole start depth'))

    def _clear_near_corners(self, pocket_clearing_centre: Tuple[float, float], final_clearing_radius: float, position: Position, operation_commands: list[GCode], options: Options) -> list[GCode]:
        precision = options.output.position_precision
        tool_options = options.tool

        br_corner_commands = []
        radial_distance_to_corner = final_clearing_radius * (sqrt(2) - 1)
        bottom_corner_radial_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

        operation_commands.append(GCode(f'Clear nearest corners in {bottom_corner_radial_stepover:.{precision}f}mm passes'))

        # Clear bottom-right corner
        br_corner_commands.extend(
            rapid_with_z_hop(
                position=position,
                new_position=Position(
                    pocket_clearing_centre[0] + final_clearing_radius,
                    position.y,
                    position.z
                ),
                job_options=options.job
            )[0]
        )

        total_radial_cut_engagement = 0
        last_cartesian_cut_engagement = 0
        while not isclose(last_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += bottom_corner_radial_stepover
            total_cartesian_cut_engagement = min(
                sqrt((final_clearing_radius + total_radial_cut_engagement) * (
                            final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius),
                final_clearing_radius)
            # Engage cut
            position.y = pocket_clearing_centre[1] - total_cartesian_cut_engagement
            br_corner_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))

            final_pass = isclose(total_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision))
            if not final_pass:
                # Arc around original clearing centre
                position.x = pocket_clearing_centre[0] + total_cartesian_cut_engagement
                position.y = pocket_clearing_centre[1] - final_clearing_radius
                br_corner_commands.append(
                    G2(x=position.x, y=position.y, i=-final_clearing_radius, j=total_cartesian_cut_engagement,
                       f=tool_options.feed_rate))
            # Disengage cut
            position.x = pocket_clearing_centre[0] + last_cartesian_cut_engagement
            br_corner_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))
            # Move to original cut start
            if not final_pass:
                br_corner_commands.extend(
                    rapid_with_z_hop(
                        position=position,
                        new_position=Position(
                            pocket_clearing_centre[0] + final_clearing_radius,
                            pocket_clearing_centre[1] - total_cartesian_cut_engagement,
                            position.z
                        ),
                        job_options=options.job
                    )[0]
                )

            last_cartesian_cut_engagement = total_cartesian_cut_engagement

        operation_commands.append(GCode('Clear first corner'))
        operation_commands.extend(br_corner_commands)
        operation_commands.append(GCode('Clear second corner'))

        corner_commands = [GCode('Clear first corner')]
        corner_commands.extend(br_corner_commands)
        corner_commands.append(GCode('Clear second corner'))
        rotation = Transformation(
            (
                lambda point: (point.y + pocket_clearing_centre[0] - pocket_clearing_centre[1]) if point.y is not None else None,
                lambda point: (pocket_clearing_centre[0] + pocket_clearing_centre[1] - point.x) if point.x is not None else None,
                lambda point: point.z if point.z is not None else None
            ),
            (
                lambda point: point.y if point.y is not None else None,
                lambda point: -point.x if point.x is not None else None,
                lambda point: point.z if point.z is not None else None
            )
        )
        for br_corner_command in br_corner_commands:
            bl_corner_command = deepcopy(br_corner_command)
            operation_commands.append(
                bl_corner_command.transform(rotation)
            )
            corner_commands.append(bl_corner_command)

        new_position = rotation.transform_absolute(position)
        position.x = new_position.x
        position.y = new_position.y

        return corner_commands

    def _clear_centre(self, pocket_clearing_centre: Tuple[float, float], final_clearing_radius: float, pocket_clearing_size: Tuple[float, float], position: Position, operation_commands: list[GCode], options: Options) -> None:
        precision = options.output.position_precision
        tool_options = options.tool

        total_arc_distance = pocket_clearing_size[1] - 2 * final_clearing_radius
        if isclose(total_arc_distance, 0, abs_tol=pow(10, -precision)):
            return

        arcing_stepover = total_arc_distance / ceil(total_arc_distance / tool_options.max_stepover)
        operation_commands.append(GCode(f'Clear centre in {arcing_stepover:.{precision}f}mm passes'))

        # Move to start position
        operation_commands.extend(
            rapid_with_z_hop(
                position=position,
                new_position=Position(
                    pocket_clearing_centre[0] - final_clearing_radius,
                    pocket_clearing_centre[1],
                    position.z
                ),
                job_options=options.job,
                comment='Move to arc start'
            )[0]
        )

        total_radial_cut_engagement = 0
        last_cartesian_stepover = 0
        while not isclose(total_radial_cut_engagement, total_arc_distance, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += arcing_stepover
            total_cartesian_stepover = sqrt((final_clearing_radius + total_radial_cut_engagement) * (
                            final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius)

            # Engage cut
            position.y = pocket_clearing_centre[1] + total_cartesian_stepover
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))
            # Traverse arc
            position.x = pocket_clearing_centre[0] + final_clearing_radius
            operation_commands.append(G2(x=position.x, y=position.y, i=final_clearing_radius, j=pocket_clearing_centre[1] - position.y, f=tool_options.feed_rate))
            # Disengage cut
            position.y = pocket_clearing_centre[1] + last_cartesian_stepover
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))

            # Move to previous start position
            operation_commands.extend(
                rapid_with_z_hop(
                    position=position,
                    new_position=Position(
                        pocket_clearing_centre[0] - final_clearing_radius,
                        pocket_clearing_centre[1] + total_cartesian_stepover,
                        position.z
                    ),
                    job_options=options.job
                )[0]
            )

            last_cartesian_stepover = total_cartesian_stepover

    def _clear_far_corners(self, pocket_clearing_centre: Tuple[float, float], final_clearing_radius: float, pocket_clearing_size: Tuple[float, float], corner_commands: list[GCode], position: Position, operation_commands: list[GCode], options: Options) -> None:
        tool_options = options.tool
        precision = options.output.position_precision

        final_arcing_radius = pocket_clearing_size[1] - final_clearing_radius

        if isclose(final_arcing_radius, final_clearing_radius, abs_tol=pow(10, -precision)):
            operation_commands.append(GCode('Clear furthest corners'))
            # Repeat existing corner commands
            rotation = Transformation(
                (
                    lambda point: (point.y + pocket_clearing_centre[0] - pocket_clearing_centre[1]) if point.y is not None else None,
                    lambda point: (pocket_clearing_centre[0] + pocket_clearing_centre[1] - point.x) if point.x is not None else None,
                    lambda point: point.z if point.z is not None else None
                ),
                (
                    lambda point: point.y if point.y is not None else None,
                    lambda point: -point.x if point.x is not None else None,
                    lambda point: point.z if point.z is not None else None
                )
            )
            for corner_command in corner_commands:
                operation_commands.append(deepcopy(corner_command).transform(rotation).transform(rotation))

            new_position = rotation.transform_absolute(rotation.transform_absolute(position))
            position.x = new_position.x
            position.y = new_position.y
            return

        radial_distance_to_corner = sqrt(final_arcing_radius * final_arcing_radius + final_clearing_radius * final_clearing_radius) - final_arcing_radius
        radial_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

        operation_commands.append(GCode(f'Clear far corners in {radial_stepover:.{precision}f}mm passes'))

        tl_corner_commands = []
        tr_corner_commands_and_positions = []

        tl_corner_commands.append(GCode('First far corner'))
        tr_corner_commands_and_positions.append([
            Position(),
            lambda point: GCode('Second far corner')
        ])

        # Move to start position
        self._record_future_rapid(
            tr_corner_commands_and_positions,
            tr_corner_commands_and_positions[-1][0],
            Position(pocket_clearing_centre[0], pocket_clearing_centre[1] + final_arcing_radius, position.z),
            options.job,
            comment='Move to arc start'
        )

        total_radial_cut_engagement = 0
        last_cartesian_stepin = sqrt(final_arcing_radius * final_arcing_radius - final_clearing_radius * final_clearing_radius)
        last_cartesian_stepout = 0
        while not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += radial_stepover
            total_radius = final_arcing_radius + total_radial_cut_engagement
            total_cartesian_stepin = sqrt(total_radius * total_radius - final_clearing_radius * final_clearing_radius)
            total_cartesian_stepout = sqrt(total_radius * total_radius - final_arcing_radius * final_arcing_radius)

            # Engage cut
            position.y = pocket_clearing_centre[1] + total_cartesian_stepin
            tl_corner_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))
            tr_corner_commands_and_positions.append([
                Position(pocket_clearing_centre[0] + total_cartesian_stepout, tr_corner_commands_and_positions[-1][0].y, position.z),
                lambda point: G1(x=point.x, y=point.y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Traverse arc
                position.x = pocket_clearing_centre[0] - total_cartesian_stepout
                j = pocket_clearing_centre[1] - position.y
                position.y = pocket_clearing_centre[1] + pocket_clearing_size[1] - final_clearing_radius
                tl_corner_commands.append(G2(x=position.x, y=position.y, i=final_clearing_radius, j=j, f=tool_options.feed_rate))

                tr_corner_commands_and_positions.append([
                    Position(pocket_clearing_centre[0] + final_clearing_radius, pocket_clearing_centre[1] + total_cartesian_stepin, position.z),
                    (lambda tmp_step: lambda point: G2(x=point.x, y=point.y, i=-tmp_step, j=-final_arcing_radius, f=tool_options.feed_rate))(total_cartesian_stepout)
                ])

            # Disengage cut
            position.x = pocket_clearing_centre[0] - last_cartesian_stepout
            tl_corner_commands.append(G1(x=position.x, y=position.y, f=tool_options.feed_rate))

            tr_corner_commands_and_positions.append([
                Position(pocket_clearing_centre[0] + final_clearing_radius, pocket_clearing_centre[1] + last_cartesian_stepin, position.z),
                lambda point: G1(x=point.x, y=point.y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Move to previous start position
                tl_corner_commands.extend(
                    rapid_with_z_hop(
                        position=position,
                        new_position=Position(
                            pocket_clearing_centre[0] - final_clearing_radius,
                            pocket_clearing_centre[1] + total_cartesian_stepin,
                            position.z
                        ),
                        job_options=options.job
                    )[0]
                )

                self._record_future_rapid(
                    tr_corner_commands_and_positions,
                    tr_corner_commands_and_positions[-1][0],
                    Position(pocket_clearing_centre[0] + total_cartesian_stepout, pocket_clearing_centre[1] + final_arcing_radius, position.z),
                    options.job,
                )

            last_cartesian_stepin = total_cartesian_stepin
            last_cartesian_stepout = total_cartesian_stepout

        operation_commands.extend(tl_corner_commands)
        for point, command in tr_corner_commands_and_positions:
            position.x = point.x
            position.y = point.y
            position.z = point.z
            operation_commands.append(command(point))

    def _record_future_rapid(self, commands_and_positions: list[Tuple[Position, Callable[[Position], GCode]]], start_position: Position, new_position: Position, job_options: JobOptions, comment: str = None) -> None:
        rapid_commands, rapid_positions = rapid_with_z_hop(
            position=start_position,
            new_position=new_position,
            job_options=job_options,
            comment=comment
        )
        for command, position in zip(rapid_commands, rapid_positions):
            commands_and_positions.append((position, (lambda tmp_command: lambda point: tmp_command)(command)))

    def _create_finishing_pass(self, centre: Tuple[float, float], pocket_final_size: Tuple[float, float], position: Position, operation_commands: list[GCode], options: Options) -> None:
        tool_options = options.tool
        precision = options.output.position_precision

        operation_commands.append(GCode(f'{tool_options.finishing_pass:.{precision}f}mm finishing pass'))

        # Feed into cut
        position.x = centre[0] + pocket_final_size[0] / 2
        operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))

        initial_y_position = position.y
        if tool_options.finishing_climb:
            position.y = centre[1] + pocket_final_size[1] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.x = centre[0] - pocket_final_size[0] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.y = centre[1] - pocket_final_size[1] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.x = centre[0] + pocket_final_size[0] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.y = initial_y_position
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
        else:
            position.y = centre[1] - pocket_final_size[1] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.x = centre[0] - pocket_final_size[0] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.y = centre[1] + pocket_final_size[1] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.x = centre[0] + pocket_final_size[0] / 2
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))
            position.y = initial_y_position
            operation_commands.append(G1(x=position.x, y=position.y, f=tool_options.finishing_feed_rate))

    def _clear_wall(self, centre: Tuple[float, float], position: Position, operation_commands: list[GCode], job_options: JobOptions) -> None:
        position.x = max(centre[0], position.x - 1)
        position.y = max(centre[1], position.y - 1)
        position.z += job_options.lead_in
        operation_commands.append(G0(x=position.x, y=position.y, z=position.z, comment='Clear wall'))

    def to_json(self) -> str:
        return (
                '{' +
                f'"width":{self._width},' +
                f'"length":{self._length},' +
                f'"depth":{self._depth},' +
                f'"centre":[{self._centre[0]},{self._centre[1]}],' +
                f'"corner":[{self._corner[0]},{self._corner[1]}],' +
                f'"start_depth":{self._start_depth},' +
                f'"finishing_pass":{str(self._finishing_pass).lower()},' +
                '}'
        ).replace(',}', '}')

    def __repr__(self) -> str:
        return (
            'RectangularPocket(' +
            f'width={self.width}, length={self.length}, ' +
            f'centre={self.centre}, corner={self.corner}, ' +
            f'depth={self.depth}, start_depth={self.start_depth}, ' +
            f'finishing_pass={self.finishing_pass}' +
            ')'
        )
