import unittest
from ddt import ddt, data

@ddt
class MainTest(unittest.TestCase):

    @data(0, 1, 2)
    def test_sample(self, value):
        self.assertLess(value, 3)