from validation_asserter import ValidationAsserter
from conversational_gcode.options.Options import Options


class TestJobOptions(ValidationAsserter):

    def setUp(self):
        self.system_under_test = Options()

    def test_initial_values(self):
        self.assertIsNotNone(self.system_under_test.job)
        self.assertIsNotNone(self.system_under_test.tool)
        self.assertIsNotNone(self.system_under_test.output)

    def test_initial_validation(self):
        self.assertSuccess(self.system_under_test)
