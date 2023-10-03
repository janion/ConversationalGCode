from math import ceil, pow, isclose

from operations.Operations import helical_plunge, spiral_out
from gcodes.GCodes import Comment, G0, G2, G3


class CircularPocket:

    def __init__(self,
                 centre: list,
                 start_depth: float,
                 diameter: float,
                 depth: float,
                 finishing_pass: bool = False):
        if diameter is None or diameter <= 0:
            raise ValueError('Pocket diameter must be positive and non-zero')
        elif depth is None or depth <= 0:
            raise ValueError('Pocket depth must be positive and non-zero')
        elif centre is None:
            raise ValueError('Pocket centre coordinates must be specified')
        elif start_depth is None:
            raise ValueError('Pocket start depth must be specified')
        self._centre = centre
        self._start_depth = start_depth
        self._diameter = diameter
        self._depth = depth
        self._finishing_pass = finishing_pass is not None and finishing_pass

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

        if self._diameter <= tool_options.tool_diameter:
            raise ValueError(
                f'Hole diameter {self._diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and roughing_diameter <= tool_options.tool_diameter:
            raise ValueError(
                f'Hole diameter {self._diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')

        final_path_radius = (roughing_diameter - tool_options.tool_diameter) / 2
        initial_path_radius = min(final_path_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_centre(position, commands, job_options)

        total_plunge = job_options.lead_in + self._depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        if final_path_radius <= tool_options.max_helix_stepover:
            # Helical interpolate to final depth as there is no need to spiral out to final diameter
            helical_plunge((self._centre[0], self._centre[1]), initial_path_radius, total_plunge, position,
                           commands, tool_options, precision)
        else:
            # Mill out material in depth steps
            final_depth = self._start_depth - self._depth
            deepest_cut_depth = position[2]
            while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                path_radius = initial_path_radius
                position[2] = deepest_cut_depth

                # Helical interpolate to depth
                helical_plunge((self._centre[0], self._centre[1]), path_radius, step_plunge, position,
                               commands, tool_options, precision)

                deepest_cut_depth = position[2]
                if not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
                    # Spiral out to final radius
                    spiral_out(path_radius, final_path_radius, position, commands, tool_options, precision)

                    # Return to centre
                    if not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                        self._clear_wall(position, commands, job_options)
                    commands.append(Comment())

        # Finishing pass
        if has_finishing_pass:
            self._create_finishing_pass(position, commands, tool_options, job_options)
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

    def _create_finishing_pass(self, position, commands, tool_options, job_options):
        commands.append(Comment(f'Finishing pass of {tool_options.finishing_pass}mm'))

        is_left = self._centre[0] > position[0]

        if is_left:
            path_radius = self._centre[0] - position[0]
            relative_centre_multiplier = 1
        else:
            path_radius = position[0] - self._centre[0]
            relative_centre_multiplier = -1

        # Spiral out to finishing depth over half turn
        position[0] += (path_radius * 2 + tool_options.finishing_pass) * relative_centre_multiplier
        relative_centre = (path_radius + tool_options.finishing_pass / 2) * relative_centre_multiplier

        finishing_command = G3 if tool_options.finishing_climb else G2

        commands.append(
            finishing_command(x=position[0], y=position[1], i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Spiral out to finishing pass'))
        # Full circle at finishing depth
        relative_centre = -(path_radius + tool_options.finishing_pass) * relative_centre_multiplier
        commands.append(
            finishing_command(x=position[0], y=position[1], i=relative_centre, f=tool_options.finishing_feed_rate,
                              comment='Complete circle at final radius'))
