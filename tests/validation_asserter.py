from unittest import TestCase


class ValidationAsserter(TestCase):

    def assertSuccess(self, system_under_test):
        """Assert that return from validate() method returns a single success item."""
        results = system_under_test.validate()
        self.assertEqual(1, len(results))
        self.assertTrue(results[0].success)

    def assertFailure(self, system_under_test, error_count: int = 1, messages: list[str] = None):
        """
        Assert that return from validate() method returns a list of failure items with the given
        messages.
        """
        results = system_under_test.validate()
        self.assertEqual(error_count, len(results))
        for i in range(error_count):
            result = results[i]
            self.assertFalse(result.success)
            if messages is not None:
                self.assertEquals(messages[i], result.message)
