import unittest
import context # allows imports directly from src

# import any extra stuff from src here as "import file_or_module"

class TestClassSample(unittest.TestCase):
    """Sample test class.

    Test classes should be named 'Test*' in files named 'test*'.
    """

    def setUp(self):
        """Runs before each test method."""
        pass

    def test_sample_test(self):
        """Sample test method.

        Test methods should be named 'test*'.
        """

        assert 1 == 1

    def tearDown(self):
        """Runs after all test methods."""
        pass
