from math import pi, ceil, tan, pow, isclose
from dataclasses import dataclass


@dataclass
class Hole:
    centre_x: float  # mm
    centre_y: float  # mm
    start_depth: float  # mm
    diameter: float  # mm
    depth: float  # mm
    finishing_pass: bool = False  # mm

    def generate(self, position, commands, tool_options, output_options):
        #########
        # Setup #
        #########
        precision = output_options.precision

        roughing_diameter = self.diameter
        has_finishing_pass = self.finishing_pass and tool_options.finishing_pass > 0

        if has_finishing_pass:
            roughing_diameter -= 2 * tool_options.finishing_pass

        if self.diameter <= tool_options.tool_diameter:
            raise ValueError(
                f'Hole diameter {self.diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and roughing_diameter <= tool_options.tool_diameter:
            raise ValueError(
                f'Hole diameter {self.diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')

        final_path_radius = (roughing_diameter - tool_options.tool_diameter) / 2
        initial_path_radius = min(final_path_radius, tool_options.max_helix_stepover)

        # Position tool ready to begin
        self._move_to_centre(position, commands, tool_options, precision)

        total_plunge = tool_options.lead_in + self.depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)

        ####################################
        # Mill out material in depth steps #
        ####################################
        final_depth = self.start_depth - self.depth
        deepest_cut_depth = position[2]
        while not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
            path_radius = initial_path_radius
            position[2] = deepest_cut_depth

            ################################
            # Helical interpolate to depth #
            ################################
            if final_path_radius <= tool_options.max_helix_stepover:
                self._helical_plunge((self.centre_x, self.centre_y), path_radius, total_plunge, position,
                                     commands, tool_options, precision)
            else:
                self._helical_plunge((self.centre_x, self.centre_y), path_radius, step_plunge, position,
                                     commands, tool_options, precision)

            deepest_cut_depth = position[2]
            if not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
                # Spiral out to final radius
                self._spiral_out(path_radius, final_path_radius, position, commands, tool_options, precision)

                # Return to centre
                if not isclose(deepest_cut_depth, final_depth, abs_tol=pow(10, -precision)):
                    self._clear_wall(position, commands, tool_options, precision)
                commands.append('')

        # Finishing pass
        if has_finishing_pass:
            self._finishing_pass(position, commands, tool_options, output_options)
        # Clear wall
        self._clear_wall(position, commands, tool_options, precision)

    def _move_to_centre(self, position, commands, tool_options, precision):
        # Position tool at hole centre
        position[0] = self.centre_x
        position[1] = self.centre_y
        commands.append(f'G0 X{position[0]:.{precision}f} Y{position[1]:.{precision}f}; Move to hole position')
        position[2] = self.start_depth + tool_options.lead_in
        commands.append(f'G0 Z{position[2]:.{precision}f}; Move to hole start depth')

    def _helical_plunge(self, centre, path_radius, plunge_depth, position, commands, tool_options, precision):
        # Position tool at 3 o'clock from hole centre
        position[0] = centre[0] + path_radius
        position[1] = centre[1]
        commands.append(
            f'G0 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f}; Move to hole start position')

        # Helically plunge to depth
        commands.append('; Helical interpolation down to step depth')
        path_circumference = 2 * pi * path_radius
        plunge_per_rev_using_angle = path_circumference * tan(tool_options.max_helix_angle * pi / 180)
        average_plunge_per_rev_using_angle = plunge_depth / ceil(plunge_depth / plunge_per_rev_using_angle)

        plunge_per_rev = min(plunge_depth, average_plunge_per_rev_using_angle)

        step_depth = position[2] - plunge_depth

        while not isclose(position[2], step_depth, abs_tol=pow(10, -precision)) and position[2] > step_depth:
            position[2] = position[2] - plunge_per_rev
            commands.append(
                f'G2 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
        commands.append(
            f'G2 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f}; Final full pass at depth')

    def _spiral_out(self, current_radius, final_path_radius, position, commands, tool_options, precision):
        radial_stepover = (final_path_radius - current_radius) / max(1, ceil(
            (final_path_radius - tool_options.max_helix_stepover) / tool_options.max_stepover))
        path_radius = current_radius

        commands.append('; Spiral out to final radius')
        while not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
            # Semi circle out increasing radius
            path_radius += radial_stepover / 2
            position[0] -= path_radius * 2
            commands.append(
                f'G2 X{position[0]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
            # Semi circle maintaining radius
            path_radius += radial_stepover / 2
            position[0] += path_radius * 2
            commands.append(
                f'G2 X{position[0]:.{precision}f} I{path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
        # Complete circle at final radius
        position[0] -= path_radius * 2
        commands.append(
            f'G2 X{position[0]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f}; Complete circle at final radius')

    def _clear_wall(self, position, commands, tool_options, precision):
        if position[0] > self.centre_x:
            position[0] = max(position[0] - 1, self.centre_x)
        else:
            position[0] = min(position[0] + 1, self.centre_x)

        position[2] += tool_options.lead_in
        commands.append(f'G0 X{position[0]:.{precision}f} Z{position[2]:.{precision}f}; Move cutter away from wall')

    def _finishing_pass(self, position, commands, tool_options, output_options):
        commands.append(f'; Finishing pass of {tool_options.finishing_pass}mm')
        precision = output_options.precision

        is_left = self.centre_x > position[0]

        if is_left:
            path_radius = self.centre_x - position[0]
            relative_centre_multiplier = 1
        else:
            path_radius = position[0] - self.centre_x
            relative_centre_multiplier = -1

        # Spiral out to finishing depth over half turn
        position[0] += (path_radius * 2 + tool_options.finishing_pass) * relative_centre_multiplier
        relative_centre = (path_radius + tool_options.finishing_pass / 2) * relative_centre_multiplier
        commands.append(
            f'G3 X{position[0]:.{precision}f} I{relative_centre:.{precision}f} J0 F{tool_options.finishing_feed_rate:.{precision}f}; Spiral out to finishing pass')
        # Full circle at finishing depth
        relative_centre = -(path_radius + tool_options.finishing_pass) * relative_centre_multiplier
        commands.append(
            f'G3 X{position[0]:.{precision}f} I{relative_centre:.{precision}f} J0 F{tool_options.finishing_feed_rate:.{precision}f}; Complete circle at final radius')

