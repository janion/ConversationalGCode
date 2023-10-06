from operations.Operations import helical_plunge
from gcodes.GCodes import Comment, G0


class CircularProfile:

    def __init__(self,
                 centre: list,
                 start_depth: float,
                 diameter: float,
                 depth: float):
        if diameter is None or diameter <= 0:
            raise ValueError('Profile diameter must be positive and non-zero')
        elif depth is None or depth <= 0:
            raise ValueError('Profile depth must be positive and non-zero')
        elif centre is None:
            raise ValueError('Profile centre coordinates must be specified')
        elif start_depth is None:
            raise ValueError('Profile start depth must be specified')
        self._centre = centre
        self._start_depth = start_depth
        self._diameter = diameter
        self._depth = depth

    def generate(self, position, commands, options):
        # Setup
        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        if self._diameter <= tool_options.tool_diameter:
            raise ValueError(
                f'Profile diameter {self._diameter}mm must be greater than tool diameter {tool_options.tool_diameter}mm')

        commands.append(Comment('Circular profile'))

        path_radius = (self._diameter - tool_options.tool_diameter) / 2

        # Position tool ready to begin
        self._move_to_centre(position, commands, job_options)

        helical_plunge(self._centre, path_radius, job_options.lead_in + self._depth, position, commands, tool_options, precision)
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
