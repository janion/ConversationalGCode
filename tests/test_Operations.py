from unittest import TestCase
from typing import Tuple

from conversational_gcode.operations.Operations import *


class TestOperationsRapidWithZHop(TestCase):

    def setUp(self):
        self.job_options = JobOptions()

    def test_origin_to_xy(self):
        comment = "Weeeeee!"
        position = Position(0, 0, 0)
        start = Position(position.x, position.y, position.z)
        end = Position(1, 2, 0)

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(3, len(commands))
        self.assertEqual(
            G0(z=end.z + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=end.x, y=end.y), commands[1])
        self.assertEqual(G0(z=end.z), commands[2])

        # Check final position
        self.assertEqual(end, position)

        # Check intermediate positions
        self.assertEqual(3, len(commands))
        self.assertEqual(Position(start.x, start.y, end.z + self.job_options.lead_in), positions[0])
        self.assertEqual(Position(end.x, end.y, end.z + self.job_options.lead_in), positions[1])
        self.assertEqual(end, positions[2])

    def test_nowhere_to_xy(self):
        comment = "Weeeeee!"
        position = Position()
        end = Position(1, 2, 0)

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(3, len(commands))
        self.assertEqual(
            G0(z=end.z + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=end.x, y=end.y), commands[1])
        self.assertEqual(G0(z=end.z), commands[2])

        # Check final position
        self.assertEqual(end, position)

        # Check intermediate positions
        self.assertEqual(3, len(commands))
        self.assertEqual(Position(end.x, end.y, end.z + self.job_options.lead_in), positions[0])
        self.assertEqual(Position(end.x, end.y, end.z + self.job_options.lead_in), positions[1])
        self.assertEqual(end, positions[2])

    def test_somewhere_to_xy_z_raise(self):
        comment = "Weeeeee!"
        position = Position(1, 2, 3)
        start = Position(position.x, position.y, position.z)
        end = Position(11, 12, 13)

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(3, len(commands))
        self.assertEqual(
            G0(z=end.z + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=end.x, y=end.y), commands[1])
        self.assertEqual(G0(z=end.z), commands[2])

        # Check final position
        self.assertEqual(end, position)

        # Check intermediate positions
        self.assertEqual(3, len(commands))
        self.assertEqual(Position(start.x, start.y, end.z + self.job_options.lead_in), positions[0])
        self.assertEqual(Position(end.x, end.y, end.z + self.job_options.lead_in), positions[1])
        self.assertEqual(end, positions[2])

    def test_somewhere_to_xy_z_drop(self):
        comment = "Weeeeee!"
        position = Position(11, 21, 13)
        start = Position(position.x, position.y, position.z)
        end = Position(1, 2, 3)

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(3, len(commands))
        self.assertEqual(
            G0(z=start.z + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=end.x, y=end.y), commands[1])
        self.assertEqual(G0(z=end.z), commands[2])

        # Check final position
        self.assertEqual(end, position)

        # Check intermediate positions
        self.assertEqual(3, len(commands))
        self.assertEqual(Position(start.x, start.y, start.z + self.job_options.lead_in), positions[0])
        self.assertEqual(Position(end.x, end.y, start.z + self.job_options.lead_in), positions[1])
        self.assertEqual(end, positions[2])

    def test_somewhere_to_same_place(self):
        comment = "Weeeeee!"
        position = Position(1, 2, 3)
        start = Position(position.x, position.y, position.z)
        end = Position(position.x, position.y, position.z)

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(0, len(commands))

        # Check final position
        self.assertEqual(end, position)

        # Check intermediate positions
        self.assertEqual(0, len(positions))


class TestOperationsHelicalPlunge(TestCase):

    def setUp(self):
        self.tool_options = ToolOptions()

    def assertPlunge(
            self,
            arc_command: type,
            centre: Tuple[float, float],
            radius: float,
            start_depth: float,
            plunge_depth: float,
            position: Position,
            commands: list[GCode]
    ):
        self.assertEqual(6, len(commands))
        self.assertEqual(
            G0(
                x=centre[0] + radius,
                y=centre[1],
                z=start_depth,
                comment='Move to hole start position'
            ),
            commands[0]
        )
        self.assertEqual(
            GCode('Helical interpolation down to step depth'),
            commands[1]
        )
        for count in range(1, 4):
            self.assertEqual(
                arc_command(
                    x=centre[0] + radius,
                    y=centre[1],
                    z=start_depth - count * self.tool_options.max_stepdown,
                    i=-radius,
                    f=self.tool_options.feed_rate
                ),
                commands[1 + count]
            )

        self.assertEqual(
            arc_command(
                x=centre[0] + radius,
                y=centre[1],
                z=start_depth - 3 * self.tool_options.max_stepdown,
                i=-radius,
                f=self.tool_options.feed_rate,
                comment='Final full pass at depth'
            ),
            commands[5]
        )

        self.assertEqual(
            Position(centre[0] + radius, centre[1], start_depth - plunge_depth),
            position
        )

    def test_internal_conventional_plunge_at_origin(self):
        commands = []
        position = Position(0, 0, 0)
        centre = (0, 0)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=True,
            is_climb=False
        )

        self.assertPlunge(
            arc_command=G2,
            centre=centre,
            radius=radius,
            start_depth=0,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_climb_plunge_at_origin(self):
        commands = []
        position = Position(0, 0, 0)
        centre = (0, 0)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=True,
            is_climb=True
        )

        self.assertPlunge(
            arc_command=G3,
            centre=centre,
            radius=radius,
            start_depth=0,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_conventional_plunge_at_origin(self):
        commands = []
        position = Position(0, 0, 0)
        centre = (0, 0)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=False,
            is_climb=False
        )

        self.assertPlunge(
            arc_command=G3,
            centre=centre,
            radius=radius,
            start_depth=0,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_climb_plunge_at_origin(self):
        commands = []
        position = Position(0, 0, 0)
        centre = (0, 0)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=False,
            is_climb=True
        )

        self.assertPlunge(
            arc_command=G2,
            centre=centre,
            radius=radius,
            start_depth=0,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_conventional_plunge_at_position(self):
        commands = []
        start_depth = 3
        position = Position(0, 0, start_depth)
        centre = (1, 2)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=True,
            is_climb=False
        )

        self.assertPlunge(
            arc_command=G2,
            centre=centre,
            radius=radius,
            start_depth=start_depth,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_climb_plunge_at_position(self):
        commands = []
        start_depth = 3
        position = Position(0, 0, start_depth)
        centre = (1, 2)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=True,
            is_climb=True
        )

        self.assertPlunge(
            arc_command=G3,
            centre=centre,
            radius=radius,
            start_depth=start_depth,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_conventional_plunge_at_position(self):
        commands = []
        start_depth = 3
        position = Position(0, 0, start_depth)
        centre = (1, 2)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=False,
            is_climb=False
        )

        self.assertPlunge(
            arc_command=G3,
            centre=centre,
            radius=radius,
            start_depth=start_depth,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_climb_plunge_at_position(self):
        commands = []
        start_depth = 3
        position = Position(0, 0, start_depth)
        centre = (1, 2)
        radius = 10
        plunge_depth = 3 * self.tool_options.max_stepdown

        helical_plunge(
            centre=centre,
            path_radius=radius,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2,
            is_inner=False,
            is_climb=True
        )

        self.assertPlunge(
            arc_command=G2,
            centre=centre,
            radius=radius,
            start_depth=start_depth,
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )


class TestOperationsSpiralOut(TestCase):

    def setUp(self):
        self.tool_options = ToolOptions()

    def assertSpiral(
            self,
            arc_command: type,
            centre: [float],
            initial_radius: float,
            final_radius: float,
            stepover: float,
            step_count: int,
            position: [float],
            commands: [GCode]
    ):
        self.assertEqual(step_count * 2 + 2, len(commands))
        self.assertEqual(
            GCode(f'Spiral out to final radius in {self.tool_options.max_stepover:.2f}mm passes'),
            commands[0]
        )
        for count in range(1, 3):
            self.assertEqual(
                arc_command(
                    x=centre[0] - (initial_radius + stepover * count),
                    y=centre[1],
                    i=-(initial_radius + stepover * (count - 0.5)),
                    f=self.tool_options.feed_rate
                ),
                commands[count * 2 - 1]
            )
            self.assertEqual(
                arc_command(
                    x=centre[0] + (initial_radius + stepover * count),
                    y=centre[1],
                    i=(initial_radius + stepover * count),
                    f=self.tool_options.feed_rate
                ),
                commands[count * 2]
            )

        self.assertEqual(
            arc_command(
                x=centre[0] - final_radius,
                y=centre[1],
                i=-final_radius,
                f=self.tool_options.feed_rate,
                comment='Complete circle at final radius'
            ),
            commands[step_count * 2 + 1]
        )

        self.assertEqual(
            Position(centre[0] - final_radius, centre[1], position.z),
            position
        )

    def test_spiral_out_at_origin(self):
        commands = []
        current_radius = 10
        final_radius = current_radius + 2 * self.tool_options.max_stepover
        centre = (0, 0)
        position = Position(centre[0] + current_radius, centre[1], 0)

        spiral_out(
            current_radius=current_radius,
            final_path_radius=final_radius,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2
        )

        self.assertSpiral(
            arc_command=G2,
            centre=centre,
            initial_radius=current_radius,
            final_radius=final_radius,
            stepover=self.tool_options.max_stepover,
            step_count=2,
            position=position,
            commands=commands
        )

    def test_spiral_out_at_position(self):
        commands = []
        current_radius = 10
        final_radius = current_radius + 2 * self.tool_options.max_stepover
        centre = (1, 2)
        position = Position(centre[0] + current_radius, centre[1], 3)

        spiral_out(
            current_radius=current_radius,
            final_path_radius=final_radius,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2
        )

        self.assertSpiral(
            arc_command=G2,
            centre=centre,
            initial_radius=current_radius,
            final_radius=final_radius,
            stepover=self.tool_options.max_stepover,
            step_count=2,
            position=position,
            commands=commands
        )


class TestOperationsSpiralIn(TestCase):

    def setUp(self):
        self.tool_options = ToolOptions()

    def assertSpiral(
            self,
            arc_command: type,
            centre: [float],
            initial_radius: float,
            final_radius: float,
            stepover: float,
            step_count: int,
            position: [float],
            commands: [GCode]
    ):
        self.assertEqual(step_count * 2 + 2, len(commands))
        self.assertEqual(
            GCode(f'Spiral in to final radius in {self.tool_options.max_stepover:.2f}mm passes'),
            commands[0]
        )
        for count in range(1, 3):
            self.assertEqual(
                arc_command(
                    x=centre[0] - (initial_radius - stepover * count),
                    y=centre[1],
                    i=-(initial_radius - stepover * (count - 0.5)),
                    f=self.tool_options.feed_rate
                ),
                commands[count * 2 - 1]
            )
            self.assertEqual(
                arc_command(
                    x=centre[0] + (initial_radius - stepover * count),
                    y=centre[1],
                    i=(initial_radius - stepover * count),
                    f=self.tool_options.feed_rate
                ),
                commands[count * 2]
            )

        self.assertEqual(
            arc_command(
                x=centre[0] - final_radius,
                y=centre[1],
                i=-final_radius,
                f=self.tool_options.feed_rate,
                comment='Complete circle at final radius'
            ),
            commands[step_count * 2 + 1]
        )

        self.assertEqual(
            Position(centre[0] - final_radius, centre[1], position.z),
            position
        )

    def test_spiral_in_at_origin(self):
        commands = []
        final_radius = 10
        current_radius = final_radius + 2 * self.tool_options.max_stepover
        centre = (0, 0)
        position = Position(centre[0] + current_radius, centre[1], 0)

        spiral_in(
            current_radius=current_radius,
            final_path_radius=final_radius,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2
        )

        self.assertSpiral(
            arc_command=G3,
            centre=centre,
            initial_radius=current_radius,
            final_radius=final_radius,
            stepover=self.tool_options.max_stepover,
            step_count=2,
            position=position,
            commands=commands
        )

    def test_spiral_in_at_position(self):
        commands = []
        final_radius = 10
        current_radius = final_radius + 2 * self.tool_options.max_stepover
        centre = (1, 2)
        position = Position(centre[0] + current_radius, centre[1], 3)

        spiral_in(
            current_radius=current_radius,
            final_path_radius=final_radius,
            position=position,
            commands=commands,
            tool_options=self.tool_options,
            precision=2
        )

        self.assertSpiral(
            arc_command=G3,
            centre=centre,
            initial_radius=current_radius,
            final_radius=final_radius,
            stepover=self.tool_options.max_stepover,
            step_count=2,
            position=position,
            commands=commands
        )
