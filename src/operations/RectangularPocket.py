from math import ceil, pow, isclose, sqrt
from copy import deepcopy
from dataclasses import dataclass

from operations.Operations import helical_plunge, spiral_out
from gcodes.GCodes import Comment, G0, G1, G2
from transform.Rotation import Rotation

from GcodeGenerator import CommandPrinter


@dataclass
class RectangularPocket:
    centre_x: float = None  # mm
    centre_y: float = None  # mm
    corner_x: float = None  # mm
    corner_y: float = None  # mm
    start_depth: float = 0  # mm
    width: float = None  # mm
    length: float = None  # mm
    depth: float = None  # mm
    # corner_radius: float = None  # mm
    finishing_pass: bool = False  # mm

    def generate(self, position, commands, options):
        #########
        # Setup #
        #########
        operation_commands = CommandPrinter(options.output)
        # operation_commands = []

        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        has_finishing_pass = self.finishing_pass and tool_options.finishing_pass > 0

        if self.width is None or self.length is None or self.depth is None:
            raise ValueError('Rectangular pocket must have width, length and depth defined.')

        if self.centre_x is not None and self.centre_y is not None:
            pocket_centre = [self.centre_x, self.centre_y]
        elif self.corner_x is not None and self.corner_y is not None:
            pocket_centre = [self.corner_x + self.width / 2, self.corner_y + self.length / 2]
        else:
            raise ValueError('Rectangular pocket must have either corner x & y, or centre x & y defined.')

        pocket_clearing_size = [self.width - tool_options.tool_diameter, self.length - tool_options.tool_diameter]
        if has_finishing_pass:
            pocket_clearing_size[0] -= tool_options.finishing_pass
            pocket_clearing_size[1] -= tool_options.finishing_pass

        rotated = False
        if self.width > self.length:
            pocket_clearing_size.reverse()
            position[0] = -position[1]
            position[1] = position[0]
            rotated = True
        pocket_clearing_centre = [pocket_centre[0], pocket_centre[1] + (pocket_clearing_size[0] - pocket_clearing_size[1]) / 2]

        if self.width <= tool_options.tool_diameter or self.length <= tool_options.tool_diameter:
            raise ValueError(
                f'Pocket size [{self.width}, {self.length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and pocket_clearing_size[0] <= 0:
            raise ValueError(
                f'Pocket size [{self.width}, {self.length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')

        final_clearing_radius = pocket_clearing_size[0] / 2
        initial_clearing_radius = min(final_clearing_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_start(pocket_clearing_centre + [self.start_depth], position, operation_commands, job_options)

        total_plunge = job_options.lead_in + self.depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        ####################################
        # Mill out material in depth steps #
        ####################################
        final_depth = self.start_depth - self.depth
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

    #     # Finishing pass
    #     if has_finishing_pass:
    #         self._finishing_pass(position, operation_commands, tool_options, job_options)
    #     # Clear wall
    #     self._clear_wall(position, operation_commands, job_options)

        if rotated:
            position[0] = position[1]
            position[1] = -position[0]
            for command in operation_commands:
                command.transform(
                    Rotation(
                        [
                            lambda x, y, z: (y + pocket_centre[0] - pocket_centre[1]) if y is not None else None,
                            lambda x, y, z: (pocket_centre[0] + pocket_centre[1] - x) if x is not None else None,
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
            [None, None],
            lambda x, y: Comment('Second far corner')
        ])

        final_arcing_radius = pocket_clearing_size[1] - final_clearing_radius
        radial_distance_to_corner = sqrt(final_arcing_radius * final_arcing_radius + final_clearing_radius * final_clearing_radius) - final_arcing_radius
        radial_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

        # Move to start position
        position[0] = pocket_clearing_centre[0] - final_clearing_radius
        position[1] = pocket_clearing_centre[1] + sqrt(final_arcing_radius * final_arcing_radius - pocket_clearing_size[0] * pocket_clearing_size[0] / 4)
        tl_corner_commands.append(G0(x=position[0], y=position[1], comment='Move to arc start'))
        tr_corner_commands_and_positions.append([
            [pocket_clearing_centre[0], pocket_clearing_centre[1] + final_arcing_radius],
            lambda x, y: G0(x=x, y=y, comment='Move to arc start')
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
                [pocket_clearing_centre[0] + total_cartesian_stepout, tr_corner_commands_and_positions[-1][0][1]],
                lambda x, y: G1(x=x, y=y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Traverse arc
                position[0] = pocket_clearing_centre[0] - total_cartesian_stepout
                j = pocket_clearing_centre[1] - position[1]
                position[1] = pocket_clearing_centre[1] + pocket_clearing_size[1] - final_clearing_radius
                tl_corner_commands.append(G2(x=position[0], y=position[1], i=final_clearing_radius, j=j, f=tool_options.feed_rate))

                tr_corner_commands_and_positions.append([
                    [pocket_clearing_centre[0] + final_clearing_radius, pocket_clearing_centre[1] + total_cartesian_stepin],
                    (lambda tmp_step: lambda x, y: G2(x=x, y=y, i=-tmp_step, j=-final_arcing_radius, f=tool_options.feed_rate))(total_cartesian_stepout)
                ])

            # Disengage cut
            position[0] = pocket_clearing_centre[0] - last_cartesian_stepout
            tl_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

            tr_corner_commands_and_positions.append([
                [tr_corner_commands_and_positions[-1][0][0], pocket_clearing_centre[1] + last_cartesian_stepin],
                lambda x, y: G1(x=x, y=y, f=tool_options.feed_rate)
            ])

            if not isclose(total_radial_cut_engagement, radial_distance_to_corner, abs_tol=pow(10, -precision)):
                # Move to previous start position
                position[0] = pocket_clearing_centre[0] - final_clearing_radius
                position[1] = pocket_clearing_centre[1] + total_cartesian_stepin
                tl_corner_commands.append(G0(x=position[0], y=position[1]))

                tr_corner_commands_and_positions.append([
                    [pocket_clearing_centre[0] + total_cartesian_stepout, pocket_clearing_centre[1] + final_arcing_radius],
                    lambda x, y: G0(x=x, y=y)
                ])

            last_cartesian_stepin = total_cartesian_stepin
            last_cartesian_stepout = total_cartesian_stepout

        operation_commands.extend(tl_corner_commands)
        for point, command in tr_corner_commands_and_positions:
            operation_commands.append(command(*point))
