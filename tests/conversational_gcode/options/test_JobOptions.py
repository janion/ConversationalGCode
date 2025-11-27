from unittest import TestCase

from conversational_gcode.validation_asserter import ValidationAsserter
from conversational_gcode.options.JobOptions import JobOptions


class TestJobOptions(ValidationAsserter):

    def setUp(self):
        self.system_under_test = JobOptions()


class TestInit(TestJobOptions):

    def test_initial_precisions(self):
        self.assertEqual(self.system_under_test.clearance_height, 10)
        self.assertEqual(self.system_under_test.lead_in, 0.25)

    def test_initial_validation(self):
        self.assertSuccess(self.system_under_test)


class TestValidation(TestJobOptions):

    def test_validation_clearance_height(self):
        self.system_under_test.clearance_height = 0
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.clearance_height = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.clearance_height = None
        self.assertFailure(self.system_under_test, 1)

    def test_validation_lead_in(self):
        self.system_under_test.lead_in = 0
        self.assertSuccess(self.system_under_test)

        self.system_under_test.lead_in = -1
        self.assertFailure(self.system_under_test, 1)

        self.system_under_test.lead_in = None
        self.assertFailure(self.system_under_test, 1)
