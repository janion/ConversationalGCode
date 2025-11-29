"""
Operations common to multiple larger operations.

Functions:
- rapid_with_z_hop()
  - A rapid move in a triangular path to prevent dragging the tool on the previously cut surface.
- helical_plunge()
  - Helical interpolation to a set depth.
- spiral_out()
  - Spiral out from a given location to a final diameter.
"""

from math import pi, ceil, tan, isclose

from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.ToolOptions import ToolOptions
from conversational_gcode.gcodes.GCodes import GCode, G0, G2, G3


def rapid_with_z_hop(
        position: list[float],
        new_position: list[float],
        job_options: JobOptions,
        comment: str = None
):
    """
    A rapid move in a triangular path to prevent dragging the tool on the previously cut surface.
    This splits the path
    in half to make the move symmetrical.
    :param position: Start position from which to move.
    :param new_position: End position to which to move.
    :param job_options: Job options from which to get hop height.
    :param comment: Optional comment to add to the first move.
    :return: The commands to perform the move, and the positions (mid and final, not start)
    """
    mid_position = [
        (position[0] + (new_position[0] - position[0]) / 2) if position[0] is not None else new_position[0],
        (position[1] + (new_position[1] - position[1]) / 2) if position[1] is not None else new_position[1],
        (max(new_position[2], position[2]) + job_options.lead_in) if position[2] is not None else new_position[2] + job_options.lead_in
    ]

    rapid_positions = []
    rapid_commands = []
    rapid_positions.append(mid_position)
    rapid_commands.append(
        G0(x=mid_position[0], y=mid_position[1], z=mid_position[2], comment=comment)
    )
    rapid_positions.append(new_position)
    rapid_commands.append(G0(x=new_position[0], y=new_position[1], z=new_position[2]))

    position[0:3] = new_position

    return rapid_commands, rapid_positions


def helical_plunge(
        centre: list[float],
        path_radius: float,
        plunge_depth: float,
        position: list[float],
        commands: list,
        tool_options: ToolOptions,
        precision: float,
        is_inner: bool = True,
        is_climb: bool = False):
    """
    Helically interpolate to a given depth.
    :param centre: XY centre of the helix.
    :param path_radius: Radius of the helical path.
    :param plunge_depth: Depth to which to plunge.
    :param position: current position of the tool. To be mutated to keep up to date.
    :param commands: List of GCode commands to which to add.
    :param tool_options: Options for the tool.
    :param precision: Positional precision to use.
    :param is_inner: True if cutting inside a diameter.
    :param is_climb: True if using a climb cut rather than a conventional cut.
    """
    # Position tool at 3 o'clock from hole centre
    position[0] = centre[0] + path_radius
    position[1] = centre[1]
    commands.append(
        G0(x=position[0], y=position[1], z=position[2], comment='Move to hole start position'))

    # Helically plunge to depth
    commands.append(GCode('Helical interpolation down to step depth'))
    path_circumference = 2 * pi * path_radius
    plunge_per_rev_using_angle = path_circumference * tan(tool_options.max_helix_angle * pi / 180)
    average_plunge_per_rev_using_angle = plunge_depth / ceil(plunge_depth / plunge_per_rev_using_angle)

    plunge_per_rev = min(plunge_depth, average_plunge_per_rev_using_angle)

    step_depth = position[2] - plunge_depth

    if is_inner == is_climb:
        command = G3
    else:
        command = G2

    while not isclose(position[2], step_depth, abs_tol=pow(10, -precision)) and position[2] > step_depth:
        position[2] = position[2] - plunge_per_rev
        commands.append(
            command(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate))
    commands.append(
        command(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate,
                comment='Final full pass at depth'))


def spiral_out(
        current_radius: float,
        final_path_radius: float,
        position: list[float],
        commands: list,
        tool_options: ToolOptions,
        precision: float):
    """
    Spiral out from a given location to a final diameter.

    Assumes that it is following a helical plunge at an initial radius.
    :param current_radius: Radius of the current path.
    :param final_path_radius: Target radius of the final path.
    :param position: current position of the tool. To be mutated to keep up to date.
    :param commands: List of GCode commands to which to add.
    :param tool_options: Options for the tool.
    :param precision: Positional precision to use.
    """
    radial_stepover = (final_path_radius - current_radius) / max(1, ceil(
        (final_path_radius - current_radius) / tool_options.max_stepover))
    path_radius = current_radius

    commands.append(
        GCode(f'Spiral out to final radius in {radial_stepover:.{precision}f}mm passes')
    )
    while not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
        # Semicircle out increasing radius
        path_radius += radial_stepover / 2
        position[0] -= path_radius * 2
        commands.append(G2(x=position[0], y=position[1], i=-path_radius, f=tool_options.feed_rate))
        # Semi circle maintaining radius
        path_radius += radial_stepover / 2
        position[0] += path_radius * 2
        commands.append(G2(x=position[0], y=position[1], i=path_radius, f=tool_options.feed_rate))
    # Complete circle at final radius
    position[0] -= path_radius * 2
    commands.append(
        G2(x=position[0], y=position[1], i=-path_radius, f=tool_options.feed_rate, comment='Complete circle at final radius'))


def spiral_in(
        current_radius: float,
        final_path_radius: float,
        position: list[float],
        commands: list,
        tool_options: ToolOptions,
        precision: float):
    """
    Spiral in from a given location to a final diameter.

    Assumes that it is following a helical plunge at an initial radius.
    :param current_radius: Radius of the current path.
    :param final_path_radius: Target radius of the final path.
    :param position: current position of the tool. To be mutated to keep up to date.
    :param commands: List of GCode commands to which to add.
    :param tool_options: Options for the tool.
    :param precision: Positional precision to use.
    """
    radial_stepover = (current_radius - final_path_radius) / max(1, ceil(
        (current_radius - final_path_radius) / tool_options.max_stepover))
    path_radius = current_radius

    commands.append(GCode(f'Spiral in to final radius in {radial_stepover:.{precision}f}mm passes'))
    while not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
        # Semicircle in decreasing radius
        path_radius -= radial_stepover / 2
        position[0] -= path_radius * 2
        commands.append(G2(x=position[0], y=position[1], i=-path_radius, f=tool_options.feed_rate))
        # Semi circle maintaining radius
        path_radius -= radial_stepover / 2
        position[0] += path_radius * 2
        commands.append(G2(x=position[0], y=position[1], i=path_radius, f=tool_options.feed_rate))
    # Complete circle at final radius
    position[0] -= path_radius * 2
    commands.append(
        G2(x=position[0], y=position[1], i=-path_radius, f=tool_options.feed_rate, comment='Complete circle at final radius'))
