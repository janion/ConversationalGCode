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
        precision = output_options.precision

        roughing_diameter = self.diameter
        has_finishing_pass = self.finishing_pass and tool_options.finishing_pass > 0

        if has_finishing_pass:
            roughing_diameter -= 2 * tool_options.finishing_pass

        if self.diameter <= tool_options.tool_diameter:
            raise ValueError(f'Hole diameter {self.diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm')
        elif has_finishing_pass and roughing_diameter <= tool_options.tool_diameter:
            raise ValueError(f'Hole diameter {self.diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm and give room for a finishing pass of {tool_options.finishing_pass}mm')
        
        final_path_radius = (roughing_diameter - tool_options.tool_diameter) / 2
        
        initial_path_radius = min(final_path_radius, tool_options.max_helix_stepover)
    
        # Position tool at hole centre
        position[0] = self.centre_x
        position[1] = self.centre_y
        commands.append(f'G0 X{position[0]:.{precision}f} Y{position[1]:.{precision}f}; Move to hole position')
        position[2] = self.start_depth + tool_options.lead_in
        commands.append(f'G0 Z{position[2]:.{precision}f}; Move to hole start depth')
    
        total_plunge = tool_options.lead_in + self.depth
        step_plunge = total_plunge / ceil(total_plunge / tool_options.max_stepdown)
        if final_path_radius <= tool_options.max_helix_stepover:
            step_plunge = total_plunge
        
        radial_stepover = (final_path_radius - initial_path_radius) / max(1, ceil((final_path_radius - tool_options.max_helix_stepover) / tool_options.max_stepover))
    
        final_depth = self.start_depth - self.depth
        while not isclose(position[2], final_depth, abs_tol = pow(10, -precision)) and position[2] > final_depth:
            path_radius = initial_path_radius
    
            # Position tool at 3 o'clock from hole centre
            position[0] = self.centre_x + path_radius
            position[1] = self.centre_y
            commands.append(f'G0 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f}; Move to hole start position')
    
            ################################
            # Helical interpolate to depth #
            ################################
            commands.append('; Helical interpolation down to step depth')
            path_circumference = 2 * pi * path_radius
            plunge_per_rev_using_angle = path_circumference * tan(tool_options.max_helix_angle * pi / 180)
            average_plunge_per_rev_using_angle = step_plunge / ceil(step_plunge / plunge_per_rev_using_angle)
            
            plunge_per_rev = min(step_plunge, average_plunge_per_rev_using_angle)
    
            step_depth = position[2] - step_plunge
    
            while not isclose(position[2], step_depth, abs_tol = pow(10, -precision)) and position[2] > step_depth:
                position[2] = position[2] - plunge_per_rev
                commands.append(f'G2 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
            commands.append(f'G2 X{position[0]:.{precision}f} Y{position[1]:.{precision}f} Z{position[2]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f}; Final full pass at depth')
    
            ######################################
            # Helical plunge was at final radius #
            ######################################
            if isclose(path_radius, final_path_radius, abs_tol = pow(10, -precision)):
                self._finishing_pass(position, commands, tool_options, output_options)
                position[0] = max(position[0] - 1, self.centre_x)
                position[2] += tool_options.lead_in
                commands.append(f'G0 X{position[0]:.{precision}f} Z{position[2]:.{precision}f}; Move cutter away from wall')

                break

            ##############################
            # Spiral out to final radius #
            ##############################
            commands.append('; Spiral out to final radius')
            while not isclose(path_radius, final_path_radius, abs_tol = pow(10, -precision)) and path_radius < final_path_radius:
                # Semi circle out increasing radius
                path_radius += radial_stepover / 2
                position[0] -= path_radius * 2
                commands.append(f'G2 X{position[0]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
                # Semi circle maintaining radius
                path_radius += radial_stepover / 2
                position[0] += path_radius * 2
                commands.append(f'G2 X{position[0]:.{precision}f} I{path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f};')
            # Complete circle at final radius        
            position[0] -= path_radius * 2
            commands.append(f'G2 X{position[0]:.{precision}f} I{-path_radius:.{precision}f} J0 F{tool_options.feed_rate:.{precision}f}; Complete circle at final radius')

            ##################
            # Finishing Pass #
            ##################

            if has_finishing_pass:
                self._finishing_pass(position, commands, tool_options, output_options)

            ####################
            # Return to centre #
            ####################

            if has_finishing_pass:
                position[0] = max(position[0] - 1, self.centre_x)
            else:
                position[0] = min(position[0] + 1, self.centre_x)

            position[2] += tool_options.lead_in
            commands.append(f'G0 X{position[0]:.{precision}f} Z{position[2]:.{precision}f}; Move cutter away from wall')
    
            commands.append('')
    
            position[2] -= tool_options.lead_in

        return commands

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

