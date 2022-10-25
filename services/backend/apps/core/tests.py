from django.test import TestCase


class DebugTestCase(TestCase):
    def test_debug(self):
        """A simple test to check if testing is well implemented."""
        hello = "world!"
        self.assertEqual(hello, "world!")
