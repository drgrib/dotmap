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

    def test_copy(self):
        dm = DotMap(self.d)
        dm_copy = dm.copy()
        self.assertIsInstance(dm_copy, DotMap)
        self.assertEqual(dm_copy.a, 1)
        self.assertEqual(dm_copy.b, 2)
        self.assertIsInstance(dm_copy.subD, DotMap)
        self.assertEqual(dm_copy.subD.c, 3)
        self.assertEqual(dm_copy.subD.d, 4)

    def test_fromkeys(self):
        dm = DotMap.fromkeys([1, 2, 3], 'a')
        self.assertEqual(len(dm), 3)
        self.assertEqual(dm[1], 'a')
        self.assertEqual(dm[2], 'a')
        self.assertEqual(dm[3], 'a')
