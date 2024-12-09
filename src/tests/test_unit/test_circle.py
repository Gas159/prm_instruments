import unittest
from .data_for_unittest_1 import circle_area
from math import pi


class TestCircleArea(unittest.TestCase):

    def test_area(self):
        self.assertEqual(circle_area(10), pi * 10**2)
        self.assertEqual(circle_area(5), pi * 5**2)
        self.assertEqual(circle_area(1), pi * 1**2)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            circle_area(-1)
            circle_area(-2)
        self.assertRaises(ValueError, circle_area, -2)

    def test_types(self):
        self.assertRaises(TypeError, circle_area, 3 + 4j)
        # self.assertRaises(TypeError, circle_area, True)
        self.assertRaises(TypeError, circle_area, [2])
        with self.assertRaises(TypeError):
            circle_area("7")
