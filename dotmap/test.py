import unittest
from __init__ import DotMap


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

    def test_dict_functionality(self):
        dm = DotMap(self.d)
        self.assertEqual(dm.get('a'), 1)
        self.assertEqual(dm.get('f', 33), 33)
        self.assertIsNone(dm.get('f'))
        self.assertTrue(dm.has_key('a'))
        self.assertFalse(dm.has_key('f'))
        dm.update([('rat', 5), ('bum', 4)], dog=7, cat=9)
        self.assertEqual(dm.rat, 5)
        self.assertEqual(dm.bum, 4)
        self.assertEqual(dm.dog, 7)
        self.assertEqual(dm.cat, 9)
        dm.update({'lol': 1, 'ba': 2})
        self.assertEqual(dm.lol, 1)
        self.assertEqual(dm.ba, 2)
