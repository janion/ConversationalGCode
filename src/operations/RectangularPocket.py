from math import ceil, pow, isclose, sqrt
from copy import deepcopy

from operations.Operations import helical_plunge, spiral_out
from gcodes.GCodes import Comment, G0, G1, G2
from transform.Rotation import Rotation


class RectangularPocket:

    def __init__(self,
                 width: float,
                 length: float,
                 depth: float,
                 centre: list = None,
                 corner: list = None,
                 start_depth: float = 0,
                 finishing_pass: bool = False):
        if width is None or width <= 0:
            raise ValueError('Pocket width must be positive and non-zero')
        elif length is None or length <= 0:
            raise ValueError('Pocket length must be positive and non-zero')
        elif depth is None or depth <= 0:
            raise ValueError('Pocket depth must be positive and non-zero')
        elif centre is None and corner is None:
            raise ValueError('Pocket corner or centre coordinates must be specified')
        elif centre is not None and corner is not None:
            raise ValueError('Pocket corner or centre coordinates must be specified, not both')
        elif start_depth is None:
            raise ValueError('Pocket start depth must be specified')

        self._width = width
        self._length = length
        self._depth = depth
        
        if centre is not None:
            self._centre = centre
        else:
            self._centre = [corner[0] + width / 2, corner[1] + length / 2]
        
        self.start_depth = start_depth
        self.finishing_pass = finishing_pass is not None and finishing_pass

    def generate(self, position, commands, options):
        #########
        # Setup #
        #########
        operation_commands = []

        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        has_finishing_pass = self.finishing_pass and tool_options.finishing_pass > 0

        if self._width is None or self._length is None or self._depth is None:
            raise ValueError('Rectangular pocket must have width, length and depth defined.')

        pocket_clearing_size = [self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter]
        pocket_final_size = [self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter]
        if has_finishing_pass:
            pocket_clearing_size[0] -= 2 * tool_options.finishing_pass
            pocket_clearing_size[1] -= 2 * tool_options.finishing_pass

        rotated = False
        if self._width > self._length:
            pocket_clearing_size.reverse()
            pocket_final_size.reverse()
            position[0] = -position[1]
            position[1] = position[0]
            rotated = True
        pocket_clearing_centre = [self._centre[0], self._centre[1] + (pocket_clearing_size[0] - pocket_clearing_size[1]) / 2]

        if self._width <= tool_options.tool_diameter or self._length <= tool_options.tool_diameter:
            raise ValueError(
                f'Pocket size [{self._width}, {self._length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and pocket_clearing_size[0] <= 0:
            raise ValueError(
                f'Pocket size [{self._width}, {self._length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')

        final_clearing_radius = pocket_clearing_size[0] / 2
        initial_clearing_radius = min(final_clearing_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_start(pocket_clearing_centre + [self.start_depth], position, operation_commands, job_options)

        total_plunge = job_options.lead_in + self._depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        ####################################
        # Mill out material in depth steps #
        ####################################
        final_depth = self.start_depth - self._depth
        deepest_cut_depth = position[2]
        while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
            clearing_radius = initial_clearing_radius
            position[2] = deepest_cut_depth

            operation_commands.append(Comment('Clear out circle at edge of pocket'))
            # Helical interpolate to depth
            helical_plunge(pocket_clearing_centre, clearing_radius, step_plunge, position,
                           operation_commands, tool_options, precision)

            # Spiral out to final radius
            deepest_cut_depth = position[2]
            if not isclose(clearing_radius, final_clearing_radius, abs_tol=pow(10, -precision)):
                spiral_out(clearing_radius, final_clearing_radius, position, operation_commands, tool_options, precision)

            # Clear bottom corners
            corner_commands = self._clear_near_corners(pocket_clearing_centre, final_clearing_radius, position, operation_commands, options)

            # Clear arcs up to edge
            self._clear_centre(pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, corner_commands, position, operation_commands, options)

            # Clear far corners
            self._clear_far_corners(pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, corner_commands, position, operation_commands, options)

        # Finishing pass
        if has_finishing_pass:
            self._finishing_pass(pocket_final_size, position, operation_commands, options)

        # Clear wall
        self._clear_wall(position, operation_commands)

        if rotated:
            position[0] = position[1]
            position[1] = -position[0]
            for command in operation_commands:
                command.transform(
                    Rotation(
                        [
                            lambda x, y, z: (y + self._centre[0] - self._centre[1]) if y is not None else None,
                            lambda x, y, z: (self._centre[0] + self._centre[1] - x) if x is not None else None,
                            lambda x, y, z: z if z is not None else None
                        ],
                        [
                            lambda x, y, z: y if y is not None else None,
                            lambda x, y, z: -x if x is not None else None,
                            lambda x, y, z: z if z is not None else None
                        ]
                    )
                )

        for operation_command in operation_commands:
            commands.append(operation_command)

    def _move_to_start(self, start_position, position, commands, job_options):
        # Position tool at hole centre
        position[0] = start_position[0]
        position[1] = start_position[1]
        commands.append(G0(x=position[0], y=position[1], comment='Move to starting position'))
        position[2] = start_position[2] + job_options.lead_in
        commands.append(G0(z=position[2], comment='Move to hole start depth'))

    def _clear_near_corners(self, pocket_clearing_centre, final_clearing_radius, position, operation_commands, options):
        precision = options.output.position_precision
        tool_options = options.tool

        operation_commands.append(Comment('Clear nearest corners'))
        br_corner_commands = []
        radial_distance_to_corner = final_clearing_radius * (sqrt(2) - 1)
        bottom_corner_radial_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

        # Clear bottom-right corner
        position[0] = pocket_clearing_centre[0] + final_clearing_radius
        br_corner_commands.append(G0(x=position[0], y=position[1]))

        total_radial_cut_engagement = 0
        last_cartesian_cut_engagement = 0
        while not isclose(last_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += bottom_corner_radial_stepover
            total_cartesian_cut_engagement = min(
                sqrt((final_clearing_radius + total_radial_cut_engagement) * (
                            final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius),
                final_clearing_radius)
            # Engage cut
            position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
            br_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

            final_pass = isclose(total_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision))
            if not final_pass:
                # Arc around original clearing centre
                position[0] = pocket_clearing_centre[0] + total_cartesian_cut_engagement
                position[1] = pocket_clearing_centre[1] - final_clearing_radius
                br_corner_commands.append(
                    G2(x=position[0], y=position[1], i=-final_clearing_radius, j=total_cartesian_cut_engagement,
                       f=tool_options.feed_rate))
            # Disengage cut
            position[0] = pocket_clearing_centre[0] + last_cartesian_cut_engagement
            br_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))
            # Move to original cut start
            if not final_pass:
                position[0] = pocket_clearing_centre[0] + final_clearing_radius
                position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
                br_corner_commands.append(G0(x=position[0], y=position[1]))

            last_cartesian_cut_engagement = total_cartesian_cut_engagement

        br_corner_commands.append(Comment('Clear first corner'))
        operation_commands.extend(br_corner_commands)
        corner_commands = []
        corner_commands.extend(br_corner_commands)
        corner_commands.append(Comment('Clear second corner'))
        rotation = Rotation(
            [
                lambda x, y, z: (y + pocket_clearing_centre[0] - pocket_clearing_centre[1]) if y is not None else None,
                lambda x, y, z: (pocket_clearing_centre[0] + pocket_clearing_centre[1] - x) if x is not None else None,
                lambda x, y, z: z if z is not None else None
            ],
            [
                lambda x, y, z: y if y is not None else None,
                lambda x, y, z: -x if x is not None else None,
                lambda x, y, z: z if z is not None else None
            ]
        )
        for br_corner_command in br_corner_commands:
            bl_corner_command = deepcopy(br_corner_command)
            operation_commands.append(
                bl_corner_command.transform(rotation)
            )
            corner_commands.append(bl_corner_command)

        new_position = rotation.transform_absolute(position)
        position[0] = new_position[0]
        position[1] = new_position[1]

        return corner_commands

    def _clear_centre(self, pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, corner_commands, position, operation_commands, options):
        precision = options.output.position_precision
        tool_options = options.tool

        operation_commands.append(Comment('Clear furthest corners'))

        total_arc_distance = pocket_clearing_size[1] - 2 * final_clearing_radius
        if isclose(total_arc_distance, 0, abs_tol=pow(10, -precision)):
            # Repeat existing corner commands
            rotation = Rotation(
                [
                    lambda x, y, z: (y + pocket_clearing_centre[0] - pocket_clearing_centre[1]) if y is not None else None,
                    lambda x, y, z: (pocket_clearing_centre[0] + pocket_clearing_centre[1] - x) if x is not None else None,
                    lambda x, y, z: z if z is not None else None
                ],
                [
                    lambda x, y, z: y if y is not None else None,
                    lambda x, y, z: -x if x is not None else None,
                    lambda x, y, z: z if z is not None else None
                ]
            )
            for corner_command in corner_commands:
                operation_commands.append(deepcopy(corner_command).transform(rotation).transform(rotation))

            new_position = rotation.transform_absolute(rotation.transform_absolute(position))
            position[0] = new_position[0]
            position[1] = new_position[1]
            return

        arcing_stepover = total_arc_distance / ceil(total_arc_distance / tool_options.max_stepover)

        # Move to start position
        position[0] = pocket_clearing_centre[0] - final_clearing_radius
        position[1] = pocket_clearing_centre[1]
        operation_commands.append(G0(x=position[0], y=pocket_clearing_centre[1], comment='Move to arc start'))

        total_radial_cut_engagement = 0
        last_cartesian_stepover = 0
        while not isclose(total_radial_cut_engagement, total_arc_distance, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += arcing_stepover
            total_cartesian_stepover = sqrt((final_clearing_radius + total_radial_cut_engagement) * (
                            final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius)

            # Engage cut
            position[1] = pocket_clearing_centre[1] + total_cartesian_stepover
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))
            # Traverse arc
            position[0] = pocket_clearing_centre[0] + final_clearing_radius
            operation_commands.append(G2(x=position[0], y=position[1], i=final_clearing_radius, j=pocket_clearing_centre[1] - position[1], f=tool_options.feed_rate))
            # Disengage cut
            position[1] = pocket_clearing_centre[1] + last_cartesian_stepover
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

            # Move to previous start position
            position[0] = pocket_clearing_centre[0] - final_clearing_radius
            position[1] = pocket_clearing_centre[1] + total_cartesian_stepover
            operation_commands.append(G0(x=position[0], y=position[1]))

            last_cartesian_stepover = total_cartesian_stepover

    def _clear_far_corners(self, pocket_clearing_centre, final_clearing_radius, pocket_clearing_size, corner_commands, position, operation_commands, options):
        tool_options = options.tool
        precision = options.output.position_precision

        operation_commands.append(Comment('Clear far corners'))

        tl_corner_commands = []
        tr_corner_commands_and_positions = []

        tl_corner_commands.append(Comment('First far corner'))
        tr_corner_commands_and_positions.append([
            [None, None, None],
            lambda x, y, z: Comment('Second far corner')
        ])

        final_arcing_radius = pocket_clearing_size[1] - final_clearing_radius
        radial_distance_to_corner = sqrt(final_arcing_radius * final_arcing_radius + final_clearing_radius * final_clearing_radius) - final_arcing_radius
        radial_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

        # Move to start position
        position[0] = pocket_clearing_centre[0] - final_clearing_radius
        position[1] = pocket_clearing_centre[1] + sqrt(final_arcing_radius * final_arcing_radius - pocket_clearing_size[0] * pocket_clearing_size[0] / 4)
        tl_corner_commands.append(G0(x=position[0], y=position[1], comment='Move to arc start'))
        tr_corner_commands_and_positions.append([
            [pocket_clearing_centre[0], pocket_clearing_centre[1] + final_arcing_radius, position[2]],
            lambda x, y, z: G0(x=x, y=y, comment='Move to arc start')
        ])

        total_radial_cut_engagement = 0
        last_cartesian_stepin = sqrt(final_arcing_radius * final_arcing_radius - final_clearing_radius * final_clearing_radius)
        last_cartesian_stepout = 0
        while not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
            total_radial_cut_engagement += radial_stepover
            total_radius = final_arcing_radius + total_radial_cut_engagement
            total_cartesian_stepin = sqrt(total_radius * total_radius - final_clearing_radius * final_clearing_radius)
            total_cartesian_stepout = sqrt(total_radius * total_radius - final_arcing_radius * final_arcing_radius)

            # Engage cut
            position[1] = pocket_clearing_centre[1] + total_cartesian_stepin
            tl_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))
            tr_corner_commands_and_positions.append([
                [pocket_clearing_centre[0] + total_cartesian_stepout, tr_corner_commands_and_positions[-1][0][1], position[2]],
                lambda x, y, z: G1(x=x, y=y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Traverse arc
                position[0] = pocket_clearing_centre[0] - total_cartesian_stepout
                j = pocket_clearing_centre[1] - position[1]
                position[1] = pocket_clearing_centre[1] + pocket_clearing_size[1] - final_clearing_radius
                tl_corner_commands.append(G2(x=position[0], y=position[1], i=final_clearing_radius, j=j, f=tool_options.feed_rate))

                tr_corner_commands_and_positions.append([
                    [pocket_clearing_centre[0] + final_clearing_radius, pocket_clearing_centre[1] + total_cartesian_stepin, position[2]],
                    (lambda tmp_step: lambda x, y, z: G2(x=x, y=y, i=-tmp_step, j=-final_arcing_radius, f=tool_options.feed_rate))(total_cartesian_stepout)
                ])

            # Disengage cut
            position[0] = pocket_clearing_centre[0] - last_cartesian_stepout
            tl_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

            tr_corner_commands_and_positions.append([
                [tr_corner_commands_and_positions[-1][0][0], pocket_clearing_centre[1] + last_cartesian_stepin, position[2]],
                lambda x, y, z: G1(x=x, y=y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Move to previous start position
                position[0] = pocket_clearing_centre[0] - final_clearing_radius
                position[1] = pocket_clearing_centre[1] + total_cartesian_stepin
                tl_corner_commands.append(G0(x=position[0], y=position[1]))

                tr_corner_commands_and_positions.append([
                    [pocket_clearing_centre[0] + total_cartesian_stepout, pocket_clearing_centre[1] + final_arcing_radius, position[2]],
                    lambda x, y, z: G0(x=x, y=y)
                ])

            last_cartesian_stepin = total_cartesian_stepin
            last_cartesian_stepout = total_cartesian_stepout

        operation_commands.extend(tl_corner_commands)
        for point, command in tr_corner_commands_and_positions:
            position[0:3] = point
            operation_commands.append(command(*point))

    def _finishing_pass(self, pocket_final_size, position, operation_commands, options):
        tool_options = options.tool

        operation_commands.append(Comment(f'{tool_options.finishing_pass}mm finishing pass'))

        # Feed into cut
        position[0] = self._centre[0] + pocket_final_size[0] / 2
        operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))

        initial_y_position = position[1]
        if tool_options.finishing_climb:
            position[1] = self._centre[1] + pocket_final_size[1] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[0] = self._centre[0] - pocket_final_size[0] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[1] = self._centre[1] - pocket_final_size[1] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[0] = self._centre[0] + pocket_final_size[0] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[1] = initial_y_position
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
        else:
            position[1] = self._centre[1] - pocket_final_size[1] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[0] = self._centre[0] - pocket_final_size[0] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[1] = self._centre[1] + pocket_final_size[1] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[0] = self._centre[0] + pocket_final_size[0] / 2
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
            position[1] = initial_y_position
            operation_commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))

    def _clear_wall(self, position, operation_commands):
        position[0] = max(self._centre[0], position[0] - 1)
        position[1] = max(self._centre[1], position[1] - 1)
        operation_commands.append(G0(x=position[0], y=position[1], comment='Clear wall'))
