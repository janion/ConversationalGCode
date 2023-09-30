from math import pi, ceil, tan, pow, isclose
from gcodes.GCodes import Comment, G0, G2


def helical_plunge(centre, path_radius, plunge_depth, position, commands, tool_options, precision):
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

    while not isclose(position[2], step_depth, abs_tol=pow(10, -precision)) and position[2] > step_depth:
        position[2] = position[2] - plunge_per_rev
        commands.append(
            G2(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate))
    commands.append(
        G2(x=position[0], y=position[1], z=position[2], i=-path_radius, f=tool_options.feed_rate,
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
        commands.append(G2(x=position[0], i=-path_radius, f=tool_options.feed_rate))
        # Semi circle maintaining radius
        path_radius += radial_stepover / 2
        position[0] += path_radius * 2
        commands.append(G2(x=position[0], i=path_radius, f=tool_options.feed_rate))
    # Complete circle at final radius
    position[0] -= path_radius * 2
    commands.append(
        G2(x=position[0], i=-path_radius, f=tool_options.feed_rate, comment='Complete circle at final radius'))
