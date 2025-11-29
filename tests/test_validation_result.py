from unittest import TestCase

from conversational_gcode.validate.validation_result import ValidationResult


class TestJobOptions(TestCase):

    def test_default_success_values(self):
        system_under_test = ValidationResult()

        self.assertTrue(system_under_test.success)
        self.assertEqual('Valid', system_under_test.message)

    def test_default_failure_values(self):
        system_under_test = ValidationResult(False)

        self.assertFalse(system_under_test.success)
        self.assertEqual('Invalid', system_under_test.message)

    def test_message_stored(self):
        message = "It's borked"
        system_under_test = ValidationResult(False, message)

        self.assertFalse(system_under_test.success)
        self.assertEqual(message, system_under_test.message)
