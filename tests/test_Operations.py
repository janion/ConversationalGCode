from unittest import TestCase

from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.ToolOptions import ToolOptions
from conversational_gcode.gcodes.GCodes import GCode, G0, G2, G3

from conversational_gcode.operations.Operations import *


class TestOperationsRapidWithZHop(TestCase):

    def setUp(self):
        self.job_options = JobOptions()

    def test_origin_to_xyz(self):
        comment = "Weeeeee!"
        position = [0, 0, 0]
        end = [1, 2, 3]

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(len(commands), 2)
        self.assertEqual(
            G0(x=0.5, y=1, z=3 + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=1, y=2, z=3), commands[1])

        # Check final position
        self.assertEqual(position, end)

        # Check intermediate positions
        self.assertEqual(len(commands), 2)
        self.assertEqual(positions[0], [0.5, 1, 3 + self.job_options.lead_in])
        self.assertEqual(positions[1], end)

    def test_nowhere_to_xyz(self):
        comment = "Weeeeee!"
        position = [None, None, None]
        end = [1, 2, 3]

        commands, positions = rapid_with_z_hop(
            position,
            end,
            self.job_options,
            comment
        )

        # Check commands
        self.assertEqual(len(commands), 2)
        self.assertEqual(
            G0(x=1, y=2, z=3 + self.job_options.lead_in, comment=comment),
            commands[0]
        )
        self.assertEqual(G0(x=1, y=2, z=3), commands[1])

        # Check final position
        self.assertEqual(position, end)

        # Check intermediate positions
        self.assertEqual(len(commands), 2)
        self.assertEqual(positions[0], [1, 2, 3 + self.job_options.lead_in])
        self.assertEqual(positions[1], end)


class TestOperationsHelicalPlunge(TestCase):

    def setUp(self):
        self.tool_options = ToolOptions()

    def assertPlunge(
            self,
            arc_command: type,
            centre: [float],
            radius: float,
            plunge_depth: float,
            position: [float],
            commands: [GCode]
    ):
        self.assertEqual(len(commands), 6)
        self.assertEqual(
            commands[0],
            G0(
                x=centre[0] + radius,
                y=centre[1],
                z=centre[2],
                comment='Move to hole start position'
            )
        )
        self.assertEqual(
            commands[1],
            GCode('Helical interpolation down to step depth')
        )
        for count in range(1, 4):
            self.assertEqual(
                commands[1 + count],
                arc_command(
                    x=centre[0] + radius,
                    y=centre[1],
                    z=centre[2] - count * self.tool_options.max_stepdown,
                    i=-radius,
                    f=self.tool_options.feed_rate
                )
            )
        self.assertEqual(
            commands[5],
            arc_command(
                x=centre[0] + radius,
                y=centre[1],
                z=centre[2] - 3 * self.tool_options.max_stepdown,
                i=-radius,
                f=self.tool_options.feed_rate,
                comment='Final full pass at depth'
            )
        )

        self.assertEqual(
            position,
            [centre[0] + radius, centre[1], centre[2] - plunge_depth]
        )

    def test_internal_conventional_plunge_at_origin(self):
        commands = []
        position = [0, 0, 0]
        centre = [0, 0, 0]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_climb_plunge_at_origin(self):
        commands = []
        position = [0, 0, 0]
        centre = [0, 0, 0]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_conventional_plunge_at_origin(self):
        commands = []
        position = [0, 0, 0]
        centre = [0, 0, 0]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_climb_plunge_at_origin(self):
        commands = []
        position = [0, 0, 0]
        centre = [0, 0, 0]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_conventional_plunge_at_position(self):
        commands = []
        position = [0, 0, 3]
        centre = [1, 2, 3]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_internal_climb_plunge_at_position(self):
        commands = []
        position = [0, 0, 3]
        centre = [1, 2, 3]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_conventional_plunge_at_position(self):
        commands = []
        position = [0, 0, 3]
        centre = [1, 2, 3]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )

    def test_external_climb_plunge_at_position(self):
        commands = []
        position = [0, 0, 3]
        centre = [1, 2, 3]
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
            plunge_depth=plunge_depth,
            position=position,
            commands=commands
        )
