import unittest
from __init__ import DotMap


class ReadmeTestCase(unittest.TestCase):
    def test_basic_use(self):
        m = DotMap()
        self.assertIsInstance(m, DotMap)
        m.name = 'Joe'
        self.assertEqual(m.name, 'Joe')
        self.assertEqual('Hello ' + m.name, 'Hello Joe')
        self.assertIsInstance(m, dict)
        self.assertTrue(issubclass(m.__class__, dict))
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

    def test_dict_conversion(self):
        d = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}}
        m = DotMap(d)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        d2 = m.toDict()
        self.assertIsInstance(d2, dict)
        self.assertNotIsInstance(d2, DotMap)
        self.assertEqual(len(d2), 3)
        self.assertEqual(d2['a'], 1)
        self.assertEqual(d2['b'], 2)
        self.assertNotIsInstance(d2['c'], DotMap)
        self.assertEqual(len(d2['c']), 2)
        self.assertEqual(d2['c']['d'], 3)
        self.assertEqual(d2['c']['e'], 4)

    def test_ordered_iteration(self):
        m = DotMap()
        m.people.john.age = 32
        m.people.john.job = 'programmer'
        m.people.mary.age = 24
        m.people.mary.job = 'designer'
        m.people.dave.age = 55
        m.people.dave.job = 'manager'
        expected = [
            ('john', 32, 'programmer'),
            ('mary', 24, 'designer'),
            ('dave', 55, 'manager'),
        ]
        for i, (k, v) in enumerate(m.people.items()):
            self.assertEqual(expected[i][0], k)
            self.assertEqual(expected[i][1], v.age)
            self.assertEqual(expected[i][2], v.job)


class BasicTestCase(unittest.TestCase):
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
        ordered_keys = [
            'a',
            'b',
            'subD',
            'rat',
            'bum',
            'dog',
            'cat',
            'lol',
            'ba',
        ]
        for i, k in enumerate(m):
            self.assertEqual(ordered_keys[i], k)
        self.assertTrue('a' in m)
        self.assertFalse('c' in m)
        ordered_values = [1, 2, DotMap(c=3, d=4), 5, 4, 7, 9, 1, 2]
        for i, v in enumerate(m.values()):
            self.assertEqual(ordered_values[i], v)
        self.assertTrue('c' in m.subD)
        self.assertTrue(len(m.subD), 2)
        del m.subD.c
        self.assertFalse('c' in m.subD)
        self.assertTrue(len(m.subD), 1)

    def test_list_comprehension(self):
        parentDict = {
            'name': 'Father1',
            'children': [
                {'name': 'Child1'},
                {'name': 'Child2'},
                {'name': 'Child3'},
            ]
        }
        parent = DotMap(parentDict)
        ordered_names = ['Child1', 'Child2', 'Child3']
        comp = [x.name for x in parent.children]
        self.assertEqual(ordered_names, comp)


class PickleTestCase(unittest.TestCase):
    def setUp(self):
        self.d = {
            'a': 1,
            'b': 2,
            'subD': {'c': 3, 'd': 4}
        }

    def test(self):
        import pickle
        pm = DotMap(self.d)
        s = pickle.dumps(pm)
        m = pickle.loads(s)
        self.assertIsInstance(m, DotMap)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        self.assertIsInstance(m.subD, DotMap)
        self.assertEqual(m.subD.c, 3)
        self.assertEqual(m.subD.d, 4)


class EmptyTestCase(unittest.TestCase):
    def test(self):
        m = DotMap()
        self.assertTrue(m.empty())
        m.a = 1
        self.assertFalse(m.empty())
        self.assertTrue(m.b.empty())
        self.assertIsInstance(m.b, DotMap)


class DynamicTestCase(unittest.TestCase):
    def test(self):
        m = DotMap()
        m.still.works
        m.sub.still.works
        nonDynamic = DotMap(_dynamic=False)

        def assignNonDynamic():
            nonDynamic.no
        self.assertRaises(KeyError, assignNonDynamic)

        nonDynamicWithInit = DotMap(m, _dynamic=False)
        nonDynamicWithInit.still.works
        nonDynamicWithInit.sub.still.works

        def assignNonDynamicWithInit():
            nonDynamicWithInit.no.creation
        self.assertRaises(KeyError, assignNonDynamicWithInit)


class RecursiveTestCase(unittest.TestCase):
    def test(self):
        m = DotMap()
        m.a = 5
        m_id = id(m)
        m.recursive = m
        self.assertEqual(id(m.recursive.recursive.recursive), m_id)
        self.assertEqual(str(m), '''DotMap(a=5, recursive=DotMap(...))''')
        d = m.toDict()
        d_id = id(d)
        d['a'] = 5
        d['recursive'] = d
        d['recursive']['recursive']['recursive']
        self.assertEqual(id(d['recursive']['recursive']['recursive']), d_id)
        self.assertEqual(str(d), '''{'a': 5, 'recursive': {...}}''')
        m2 = DotMap(d)
        m2_id = id(m2)
        self.assertEqual(id(m2.recursive.recursive.recursive), m2_id)
        self.assertEqual(str(m2), '''DotMap(a=5, recursive=DotMap(...))''')


class kwargTestCase(unittest.TestCase):
    def test(self):
        a = {'1': 'a', '2': 'b'}
        b = DotMap(a, _dynamic=False)

        def capture(**kwargs):
            return kwargs
        self.assertEqual(a, capture(**b.toDict()))


class DeepCopyTestCase(unittest.TestCase):
    def test(self):
        import copy
        original = DotMap()
        original.a = 1
        original.b = 3
        shallowCopy = original
        deepCopy = copy.deepcopy(original)
        self.assertEqual(original, shallowCopy)
        self.assertEqual(id(original), id(shallowCopy))
        self.assertEqual(original, deepCopy)
        self.assertNotEqual(id(original), id(deepCopy))
        original.a = 2
        self.assertEqual(original, shallowCopy)
        self.assertNotEqual(original, deepCopy)

    def test_order_preserved(self):
        import copy
        original = DotMap()
        original.a = 1
        original.b = 2
        original.c = 3
        deepCopy = copy.deepcopy(original)
        orderedPairs = []
        for k, v in original.iteritems():
            orderedPairs.append((k, v))
        for i, (k, v) in enumerate(deepCopy.iteritems()):
            self.assertEqual(k, orderedPairs[i][0])
            self.assertEqual(v, orderedPairs[i][1])


class DotMapTupleToDictTestCase(unittest.TestCase):
    def test(self):
        m = DotMap({'a': 1, 'b': (11, 22, DotMap({'c': 3}))})
        d = m.toDict()
        self.assertEqual(d, {'a': 1, 'b': (11, 22, {'c': 3})})


class OrderedDictInitTestCase(unittest.TestCase):
    def test(self):
        from collections import OrderedDict
        o = OrderedDict([('a', 1), ('b', 2), ('c', [OrderedDict([('d', 3)])])])
        m = DotMap(o)
        self.assertIsInstance(m, DotMap)
        self.assertIsInstance(m.c[0], DotMap)


class EmptyAddTestCase(unittest.TestCase):
    def test_base(self):
        m = DotMap()
        m.a.label = 'test'
        m.a.counter += 2
        self.assertIsInstance(m.a, DotMap)
        self.assertEqual(m.a.label, 'test')
        self.assertNotIsInstance(m.a.counter, DotMap)
        self.assertIsInstance(m.a.counter, int)
        self.assertEqual(m.a.counter, 2)
        m.a.counter += 1

    def test_proposal(self):
        my_counters = DotMap()
        pages = [
            'once upon a time',
            'there was like this super awesome prince',
            'and there was this super rad princess',
            'and they had a mutually respectful, egalitarian relationship',
            'the end'
        ]
        for stuff in pages:
            my_counters.page += 1
        self.assertIsInstance(my_counters, DotMap)
        self.assertNotIsInstance(my_counters.page, DotMap)
        self.assertIsInstance(my_counters.page, int)
        self.assertEqual(my_counters.page, 5)

    def test_string_addition(self):
        m = DotMap()
        m.quote += 'lions'
        m.quote += ' and tigers'
        m.quote += ' and bears'
        m.quote += ', oh my'
        self.assertEqual(m.quote, 'lions and tigers and bears, oh my')

    def test_strange_addition(self):
        m = DotMap()
        m += "I'm a string now"
        self.assertIsInstance(m, str)
        self.assertNotIsInstance(m, DotMap)
        self.assertEqual(m, "I'm a string now")

    def test_type_error_raised(self):
        m = DotMap()

        def badAddition():
            m.a += 1
            m.a += ' and tigers'
        self.assertRaises(TypeError, badAddition)
