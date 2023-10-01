from math import ceil, pow, isclose, sqrt
from copy import deepcopy
from dataclasses import dataclass

from operations.Operations import helical_plunge, spiral_out
from gcodes.GCodes import Comment, G0, G1, G2, G3
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
        # operation_commands = CommandPrinter(options.output)
        operation_commands = []

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

        pocket_path_size = [self.width - tool_options.tool_diameter, self.length - tool_options.tool_diameter]
        if has_finishing_pass:
            pocket_path_size[0] -= tool_options.finishing_pass
            pocket_path_size[1] -= tool_options.finishing_pass

        rotated = False
        if self.width > self.length:
            # pocket_centre.reverse()
            pocket_path_size.reverse()
            position[0] = -position[1]
            position[1] = position[0]
            rotated = True
        pocket_clearing_centre = [pocket_centre[0], pocket_centre[1] + (pocket_path_size[0] - pocket_path_size[1]) / 2]

        if self.width <= tool_options.tool_diameter or self.length <= tool_options.tool_diameter:
            raise ValueError(
                f'Pocket size [{self.width}, {self.length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and pocket_path_size[0] <= 0:
            raise ValueError(
                f'Pocket size [{self.width}, {self.length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')

        final_clearing_radius = pocket_path_size[0] / 2
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
            br_corner_commands = []
            br_corner_commands.append(Comment('Clear nearest corners'))
            radial_distance_to_corner = final_clearing_radius * (sqrt(2) - 1)
            bottom_corner_stepover = radial_distance_to_corner / ceil(radial_distance_to_corner / tool_options.max_stepover)

            # Clear bottom-right corner
            position[0] = pocket_clearing_centre[0] + final_clearing_radius
            br_corner_commands.append(G0(x=position[0], y=position[1], comment='Move to bottom-right corner'))

            total_radial_cut_engagement = 0
            last_cartesian_cut_engagement = 0
            while not isclose(last_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
                total_radial_cut_engagement += bottom_corner_stepover
                total_cartesian_cut_engagement = min(
                    sqrt((final_clearing_radius + total_radial_cut_engagement) * (final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius),
                    final_clearing_radius)
                # Engage cut
                position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
                br_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))

                if not isclose(total_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
                    # Arc around original clearing centre
                    position[0] = pocket_clearing_centre[0] + total_cartesian_cut_engagement
                    position[1] = pocket_clearing_centre[1] - final_clearing_radius
                    br_corner_commands.append(G2(x=position[0], y=position[1], i=-pocket_path_size[0] / 2, j=total_cartesian_cut_engagement, f=tool_options.feed_rate))
                # Disengage cut
                position[0] = pocket_clearing_centre[0] + last_cartesian_cut_engagement
                br_corner_commands.append(G1(x=position[0], y=position[1], f=tool_options.feed_rate))
                # Move to original cut start
                position[0] = pocket_clearing_centre[0] + final_clearing_radius
                position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
                br_corner_commands.append(G0(x=position[0], y=position[1]))

                last_cartesian_cut_engagement = total_cartesian_cut_engagement

            operation_commands.extend(br_corner_commands)
            for br_corner_command in br_corner_commands:
                bl_corner_command = deepcopy(br_corner_command)
                operation_commands.append(
                    bl_corner_command.transform(
                        Rotation(
                            [
                                lambda x, y: (y + pocket_clearing_centre[0] - pocket_clearing_centre[1]) if y is not None else None,
                                lambda x, y: (pocket_clearing_centre[0] + pocket_clearing_centre[1] - x) if x is not None else None
                            ],
                            [
                                lambda x, y: y if y is not None else None,
                                lambda x, y: -x if x is not None else None
                            ]
                        )
                    )
                )


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
                            lambda x, y: (y + pocket_centre[0] - pocket_centre[1]) if y is not None else None,
                            lambda x, y: (pocket_centre[0] + pocket_centre[1] - x) if x is not None else None
                        ],
                        [
                            lambda x, y: y if y is not None else None,
                            lambda x, y: -x if x is not None else None
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

    # def _clear_corner(self, position, commands, options):
    #     if position[0] != pocket_clearing_centre[0] + final_clearing_radius:
    #         position[0] = pocket_clearing_centre[0] + final_clearing_radius
    #         operation_commands.append(G0(x=position[0], comment='Move to bottom-right corner'))
    #
    #     total_radial_cut_engagement = 0
    #     last_cartesian_cut_engagement = 0
    #     while not isclose(last_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
    #         total_radial_cut_engagement += bottom_corner_stepover
    #         total_cartesian_cut_engagement = min(
    #             sqrt((final_clearing_radius + total_radial_cut_engagement) * (final_clearing_radius + total_radial_cut_engagement) - final_clearing_radius * final_clearing_radius),
    #             final_clearing_radius)
    #         # Engage cut
    #         position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
    #         operation_commands.append(G1(y=position[1], f=tool_options.feed_rate))
    #
    #         if not isclose(total_cartesian_cut_engagement, final_clearing_radius, abs_tol=pow(10, -precision)):
    #             # Arc around original clearing centre
    #             position[0] = pocket_clearing_centre[0] + total_cartesian_cut_engagement
    #             position[1] = pocket_clearing_centre[1] - final_clearing_radius
    #             operation_commands.append(G2(x=position[0], y=position[1], i=-pocket_path_size[0] / 2, j=total_cartesian_cut_engagement, f=tool_options.feed_rate))
    #         # Disengage cut
    #         position[0] = pocket_clearing_centre[0] + last_cartesian_cut_engagement
    #         operation_commands.append(G1(x=position[0], f=tool_options.feed_rate))
    #         # Move to original cut start
    #         position[0] = pocket_clearing_centre[0] + final_clearing_radius
    #         position[1] = pocket_clearing_centre[1] - total_cartesian_cut_engagement
    #         operation_commands.append(G0(x=position[0], y=position[1]))
    #
    #         last_cartesian_cut_engagement = total_cartesian_cut_engagement
