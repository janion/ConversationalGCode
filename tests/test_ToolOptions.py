from validation_asserter import ValidationAsserter
from conversational_gcode.options.ToolOptions import ToolOptions


class TestToolOptions(ValidationAsserter):

    def setUp(self):
        self.system_under_test = ToolOptions()


class TestInit(TestToolOptions):

    def test_initial_precisions(self):
        self.assertEqual(self.system_under_test.tool_flutes, 44)
        self.assertEqual(self.system_under_test.tool_diameter, 6)

        self.assertEqual(self.system_under_test.spindle_speed, 1000)
        self.assertEqual(self.system_under_test.feed_rate, 100)

        self.assertEqual(self.system_under_test.max_stepover, 2)
        self.assertEqual(self.system_under_test.max_stepdown, 3)

        self.assertEqual(self.system_under_test.max_helix_stepover, 2)
        self.assertEqual(self.system_under_test.helix_feed_rate, 100)
        self.assertEqual(self.system_under_test.max_helix_angle, 3)

        self.assertEqual(self.system_under_test.finishing_pass, 0)
        self.assertEqual(self.system_under_test.finishing_feed_rate, 100)
        self.assertEqual(self.system_under_test.finishing_climb, True)

    def test_initial_validation(self):
        self.assertSuccess(self.system_under_test)


class TestValidation(TestToolOptions):

    def test_validation_tool_flutes(self):
        self.system_under_test.tool_flutes = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.tool_flutes = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.tool_flutes = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_tool_diameter(self):
        self.system_under_test.tool_diameter = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.tool_diameter = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.tool_diameter = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_spindle_speed(self):
        self.system_under_test.spindle_speed = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.spindle_speed = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.spindle_speed = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_feed_rate(self):
        self.system_under_test.feed_rate = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.feed_rate = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.feed_rate = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_max_stepover(self):
        self.system_under_test.max_stepover = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_stepover = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_stepover = None
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_stepover = self.system_under_test.tool_diameter
        self.assertSuccess(self.system_under_test)

        self.system_under_test.max_stepover = self.system_under_test.tool_diameter * 2
        self.assertFailure(self.system_under_test, 1)

    def test_validation_max_stepdown(self):
        self.system_under_test.max_stepdown = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_stepdown = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_stepdown = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_max_helix_stepover(self):
        self.system_under_test.max_helix_stepover = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_helix_stepover = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_helix_stepover = None
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_helix_stepover = self.system_under_test.tool_diameter / 2
        self.assertSuccess(self.system_under_test)

        self.system_under_test.max_helix_stepover = self.system_under_test.tool_diameter
        self.assertFailure(self.system_under_test, 1)

    def test_validation_helix_feed_rate(self):
        self.system_under_test.helix_feed_rate = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.helix_feed_rate = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.helix_feed_rate = None
        self.assertSuccess(self.system_under_test)

    def test_validation_max_helix_angle(self):
        self.system_under_test.max_helix_angle = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_helix_angle = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.max_helix_angle = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_finishing_pass(self):
        self.system_under_test.finishing_pass = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.finishing_pass = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.finishing_pass = None
        self.assertSuccess(self.system_under_test)

        self.system_under_test.finishing_pass = self.system_under_test.tool_diameter
        self.assertSuccess(self.system_under_test)

        self.system_under_test.finishing_pass = self.system_under_test.tool_diameter * 2
        self.assertFailure(self.system_under_test, 1)

    def test_validation_finishing_feed_rate(self):
        self.system_under_test.feed_rate = None

        self.system_under_test.finishing_feed_rate = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.finishing_feed_rate = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.finishing_feed_rate = None
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.feed_rate = 100
        self.assertSuccess(self.system_under_test)
