from unittest import TestCase

from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.operations.Operations import rapid_with_z_hop
from conversational_gcode.gcodes.GCodes import G0


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
