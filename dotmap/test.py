import unittest
from __init__ import DotMap


class ReadmeTestCase(unittest.TestCase):
    '''Tests examples in README.md'''

    def test_basic_use(self):
        m = DotMap()
        self.assertIsInstance(m, DotMap)
        m.name = 'Joe'
        self.assertEqual(m.name, 'Joe')
        self.assertEqual('Hello ' + m.name, 'Hello Joe')
        self.assertIsInstance(m, dict)
        self.assertEqual(m['name'], 'Joe')
        m.name += ' Smith'
        m['name'] += ' Jr'
        self.assertEqual(m.name, 'Joe Smith Jr')

    def test_automatic_hierarchy(self):
        m = DotMap()
        m.people.steve.age = 31
        self.assertEqual(m.people.steve.age, 31)

    def test_key_init(self):
        m = DotMap(a=1, b=2)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)

    def test_dict_init(self):
        d = {'a': 1, 'b': 2}
        m = DotMap(d)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        d2 = m.toDict()
        self.assertIsInstance(d2, dict)
        self.assertNotIsInstance(d2, DotMap)
        self.assertEqual(len(d2), 2)
        self.assertEqual(d2['a'], 1)
        self.assertEqual(d2['b'], 2)


class BaseTestCase(unittest.TestCase):
    '''Tests basic functionality'''

    def setUp(self):
        self.d = {
            'a': 1,
            'b': 2,
            'subD': {'c': 3, 'd': 4}
        }

    def test_dict_init(self):
        m = DotMap(self.d)
        self.assertIsInstance(m, DotMap)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        self.assertIsInstance(m.subD, DotMap)
        self.assertEqual(m.subD.c, 3)
        self.assertEqual(m.subD.d, 4)

    def test_copy(self):
        m = DotMap(self.d)
        dm_copy = m.copy()
        self.assertIsInstance(dm_copy, DotMap)
        self.assertEqual(dm_copy.a, 1)
        self.assertEqual(dm_copy.b, 2)
        self.assertIsInstance(dm_copy.subD, DotMap)
        self.assertEqual(dm_copy.subD.c, 3)
        self.assertEqual(dm_copy.subD.d, 4)

    def test_fromkeys(self):
        m = DotMap.fromkeys([1, 2, 3], 'a')
        self.assertEqual(len(m), 3)
        self.assertEqual(m[1], 'a')
        self.assertEqual(m[2], 'a')
        self.assertEqual(m[3], 'a')

    def test_dict_functionality(self):
        m = DotMap(self.d)
        self.assertEqual(m.get('a'), 1)
        self.assertEqual(m.get('f', 33), 33)
        self.assertIsNone(m.get('f'))
        self.assertTrue(m.has_key('a'))
        self.assertFalse(m.has_key('f'))
        m.update([('rat', 5), ('bum', 4)], dog=7, cat=9)
        self.assertEqual(m.rat, 5)
        self.assertEqual(m.bum, 4)
        self.assertEqual(m.dog, 7)
        self.assertEqual(m.cat, 9)
        m.update({'lol': 1, 'ba': 2})
        self.assertEqual(m.lol, 1)
        self.assertEqual(m.ba, 2)
