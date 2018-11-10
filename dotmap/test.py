import unittest
from dotmap import DotMap


class BasicTestCase(unittest.TestCase):
    '''Tests basic functionality'''

    def setUp(self):
        self.d = {
            'a': 1,
            'b': 2,
            'subD': {'c': 3, 'd': 4}
        }

    def test_dict_init(self):
        dm = DotMap(self.d)
        self.assertIsInstance(dm, DotMap)
        self.assertEqual(dm.a, 1)
        self.assertEqual(dm.b, 2)
        self.assertIsInstance(dm.subD, DotMap)
        self.assertEqual(dm.subD.c, 3)
        self.assertEqual(dm.subD.d, 4)
