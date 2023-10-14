from math import ceil, tan, pi, isclose, pow

from conversational_gcode.gcodes.GCodes import Comment, G0, G1


class RectangularProfile:

    def __init__(self,
                 width: float,
                 length: float,
                 depth: float,
                 centre: list = None,
                 corner: list = None,
                 start_depth: float = 0,
                 is_inner: bool = None):
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
        elif is_inner is None:
            raise ValueError('Profile must be specified as either inner or outer (True = inner, False = outer)')

        self._width = width
        self._length = length
        self._depth = depth

        if centre is not None:
            self._centre = centre
        else:
            self._centre = [corner[0] + width / 2, corner[1] + length / 2]
        
        self._start_depth = start_depth
        self._is_inner = is_inner

    def generate(self, position, commands, options):
        # Setup
        precision = options.output.position_precision
        tool_options = options.tool
        job_options = options.job

        if self._is_inner and (self._width <= tool_options.tool_diameter or self._length <= tool_options.tool_diameter):
            raise ValueError(
                f'Pocket size [{self._width}, {self._length}]mm must be greater than tool diameter {tool_options.tool_diameter}mm')

        if self._is_inner:
            pocket_final_size = [self._width - tool_options.tool_diameter, self._length - tool_options.tool_diameter]
        else:
            pocket_final_size = [self._width + tool_options.tool_diameter, self._length + tool_options.tool_diameter]

        total_plunge = job_options.lead_in + self._depth
        total_xy_travel = sum(pocket_final_size) * 2

        max_plunge_per_step_using_angle = total_xy_travel * tan(tool_options.max_helix_angle * pi / 180)
        plunge_per_step_using_angle = total_plunge / ceil(total_plunge / max_plunge_per_step_using_angle)

        max_plunge_per_step = min(tool_options.max_stepdown, plunge_per_step_using_angle)
        step_plunge = total_plunge / ceil(total_plunge / max_plunge_per_step)

        # Position tool
        position[0] = self._centre[0] + pocket_final_size[0] / 2
        position[1] = self._centre[1] + pocket_final_size[1] / 2
        commands.append(G0(x=position[0], y=position[1], comment='Move to starting position'))
        position[2] = self._start_depth + job_options.lead_in
        commands.append(G0(z=position[2], comment='Move to start depth'))

        x_travel_plunge = step_plunge * pocket_final_size[0] / total_xy_travel
        y_travel_plunge = step_plunge * pocket_final_size[1] / total_xy_travel

        if self._is_inner:
            travels = [
                [0, -pocket_final_size[1], -y_travel_plunge],
                [-pocket_final_size[0], 0, -x_travel_plunge],
                [0, pocket_final_size[1], -y_travel_plunge],
                [pocket_final_size[0], 0, -x_travel_plunge]
            ]
        else:
            travels = [
                [-pocket_final_size[0], 0, -x_travel_plunge],
                [0, -pocket_final_size[1], -y_travel_plunge],
                [pocket_final_size[0], 0, -x_travel_plunge],
                [0, pocket_final_size[1], -y_travel_plunge]
            ]

        while not isclose(position[2], self._start_depth - self._depth, abs_tol=pow(10, -precision)):
            for travel in travels:
                position[0] += travel[0]
                position[1] += travel[1]
                position[2] += travel[2]
                commands.append(G1(x=position[0], y=position[1], z=position[2], f=tool_options.finishing_feed_rate))

        commands.append(Comment('Final pass at full depth'))
        for travel in travels:
            position[0] += travel[0]
            position[1] += travel[1]
            commands.append(G1(x=position[0], y=position[1], f=tool_options.finishing_feed_rate))
