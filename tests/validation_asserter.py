from unittest import TestCase


class ValidationAsserter(TestCase):

    def assertSuccess(self, system_under_test):
        """Assert that return from validate() method returns a single success item."""
        results = system_under_test.validate()
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].success)

    def assertFailure(self, system_under_test, error_count: int, messages: list[str] = None):
        """Assert that return from validate() method returns a list of failure items with the given messages."""
        results = system_under_test.validate()
        self.assertEqual(len(results), error_count)
        for i in range(error_count):
            result = results[i]
            self.assertFalse(result.success)
            if messages is not None:
                self.assertEquals(result.message, messages[i])
