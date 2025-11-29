from validation_asserter import ValidationAsserter
from conversational_gcode.options.JobOptions import JobOptions


class TestJobOptions(ValidationAsserter):

    def setUp(self):
        self.system_under_test = JobOptions()

    def test_initial_values(self):
        self.assertEqual(self.system_under_test.clearance_height, 10)
        self.assertEqual(self.system_under_test.lead_in, 0.25)

    def test_initial_validation(self):
        self.assertSuccess(self.system_under_test)

    def test_validation_clearance_height(self):
        self.system_under_test.clearance_height = 0
        self.assertFailure(self.system_under_test)

        self.system_under_test.clearance_height = -1
        self.assertFailure(self.system_under_test)

        self.system_under_test.clearance_height = None
        self.assertFailure(self.system_under_test)

    def test_validation_lead_in(self):
        self.system_under_test.lead_in = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.lead_in = -1
        self.assertFailure(self.system_under_test)

        self.system_under_test.lead_in = None
        self.assertFailure(self.system_under_test)
