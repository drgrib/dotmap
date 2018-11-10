import unittest
from dotmap import DotMap

d = {
    'a': 1,
    'b': 2,
    'subD': {'c': 3, 'd': 4}
}

dm = DotMap(d)


class BasicTestCase(unittest.TestCase):
    '''Tests basic functionality'''

    def test_print(self):
        self.assertEqual(dm.a, 1)
        self.assertEqual(dm.b, 2)
