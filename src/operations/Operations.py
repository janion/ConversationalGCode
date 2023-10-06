from math import pi, ceil, tan, pow, isclose
from gcodes.GCodes import Comment, G0, G2, G3


def rapid_with_z_hop(position, new_position, job_options, comment=None):
    mid_position = [
        (position[0] + (new_position[0] - position[0]) / 2) if position[0] is not None else new_position[0],
        (position[1] + (new_position[1] - position[1]) / 2) if position[1] is not None else new_position[1],
        (max(new_position[2], position[2]) + job_options.lead_in) if position[2] is not None else new_position[2] + job_options.lead_in
    ]

    rapid_positions = []
    rapid_commands = []
    rapid_positions.append(mid_position)
    rapid_commands.append(G0(x=mid_position[0], y=mid_position[1], z=mid_position[2], comment=comment))
    rapid_positions.append(new_position)
    rapid_commands.append(G0(x=new_position[0], y=new_position[1], z=new_position[2]))

    position[0:3] = new_position

    return rapid_commands, rapid_positions


def helical_plunge(centre, path_radius, plunge_depth, position, commands, tool_options, precision, is_inner=True):
    # Position tool at 3 o'clock from hole centre
    position[0] = centre[0] + path_radius
    position[1] = centre[1]
    commands.append(
        G0(x=position[0], y=position[1], z=position[2], comment='Move to hole start position'))

    # Helically plunge to depth
    commands.append(Comment('Helical interpolation down to step depth'))
    path_circumference = 2 * pi * path_radius
    plunge_per_rev_using_angle = path_circumference * tan(tool_options.max_helix_angle * pi / 180)
    average_plunge_per_rev_using_angle = plunge_depth / ceil(plunge_depth / plunge_per_rev_using_angle)

    plunge_per_rev = min(plunge_depth, average_plunge_per_rev_using_angle)

    step_depth = position[2] - plunge_depth

    if is_inner:
        command = G2
    else:
        command = G3

    while not isclose(position[2], step_depth, abs_tol=pow(10, -precision)) and position[2] > step_depth:
        position[2] = position[2] - plunge_per_rev
        commands.append(
            command(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate))
    commands.append(
        command(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate,
                comment='Final full pass at depth'))


def spiral_out(current_radius, final_path_radius, position, commands, tool_options, precision):
    radial_stepover = (final_path_radius - current_radius) / max(1, ceil(
        (final_path_radius - tool_options.max_helix_stepover) / tool_options.max_stepover))
    path_radius = current_radius

    commands.append(Comment('Spiral out to final radius'))
    while not isclose(path_radius, final_path_radius, abs_tol=pow(10, -precision)):
        # Semi circle out increasing radius
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
