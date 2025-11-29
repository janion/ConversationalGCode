from validation_asserter import ValidationAsserter
from conversational_gcode.options.OutputOptions import OutputOptions


class TestOutputOptions(ValidationAsserter):

    def setUp(self):
        self.system_under_test = OutputOptions()

    def test_initial_values(self):
        self.assertEqual(3, self.system_under_test.position_precision)
        self.assertEqual(2, self.system_under_test.feed_precision)
        self.assertEqual(1, self.system_under_test.speed_precision)

    def test_initial_validation(self):
        self.assertSuccess(self.system_under_test)

    def test_validation_position_precision(self):
        self.system_under_test.position_precision = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.position_precision = -1
        self.assertFailure(self.system_under_test)

        self.system_under_test.position_precision = None
        self.assertFailure(self.system_under_test)

    def test_validation_feed_precision(self):
        self.system_under_test.feed_precision = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.feed_precision = -1
        self.assertFailure(self.system_under_test)

        self.system_under_test.feed_precision = None
        self.assertFailure(self.system_under_test)

    def test_validation_speed_precision(self):
        self.system_under_test.speed_precision = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.speed_precision = -1
        self.assertFailure(self.system_under_test)

        self.system_under_test.speed_precision = None
        self.assertFailure(self.system_under_test)
