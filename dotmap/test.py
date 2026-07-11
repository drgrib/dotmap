import copy
import pickle
import unittest
from collections import OrderedDict
from contextlib import redirect_stdout
from io import StringIO

from dotmap import DotMap, StaticDotMap


class TestReadme(unittest.TestCase):
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


class TestBasic(unittest.TestCase):
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
        self.assertTrue('a' in m)
        self.assertFalse('c' in m)
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


class TestPickle(unittest.TestCase):
    def setUp(self):
        self.d = {
            'a': 1,
            'b': 2,
            'subD': {'c': 3, 'd': 4}
        }

    def test(self):
        pm = DotMap(self.d)
        s = pickle.dumps(pm)
        m = pickle.loads(s)
        self.assertIsInstance(m, DotMap)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        self.assertIsInstance(m.subD, DotMap)
        self.assertEqual(m.subD.c, 3)
        self.assertEqual(m.subD.d, 4)


class TestEmpty(unittest.TestCase):
    def test(self):
        m = DotMap()
        self.assertTrue(m.empty())
        m.a = 1
        self.assertFalse(m.empty())
        self.assertTrue(m.b.empty())
        self.assertIsInstance(m.b, DotMap)


class TestDynamic(unittest.TestCase):
    def test(self):
        m = DotMap()
        m.still.works
        m.sub.still.works
        nonDynamic = DotMap(_dynamic=False)

        def assignNonDynamicAttribute():
            nonDynamic.no
        self.assertRaises(AttributeError, assignNonDynamicAttribute)

        def assignNonDynamicKey():
            nonDynamic['no']
        self.assertRaises(KeyError, assignNonDynamicKey)

        nonDynamicWithInit = DotMap(m, _dynamic=False)
        nonDynamicWithInit.still.works
        nonDynamicWithInit.sub.still.works

        def assignNonDynamicAttributeWithInit():
            nonDynamicWithInit.no.creation
        self.assertRaises(AttributeError, assignNonDynamicAttributeWithInit)

        def assignNonDynamicKeyWithInit():
            nonDynamicWithInit['no'].creation
        self.assertRaises(KeyError, assignNonDynamicKeyWithInit)

    def test_none_means_non_dynamic(self):
        m = DotMap({'a': 1}, _dynamic=None)
        self.assertEqual(m.a, 1)
        with self.assertRaises(AttributeError):
            m.missing


class TestDefault(unittest.TestCase):
    def test_missing_attribute_returns_default(self):
        address = {'city': 'abc', 'country': 'XY', 'CountryCode': 101}
        m = DotMap(address, _default_factory=str)

        self.assertEqual(m.city, 'abc')
        self.assertEqual(m.CountryCode, 101)
        self.assertNotIn('zipCode', m)
        self.assertEqual(m.zipCode, '')

    def test_nested_maps_inherit_default(self):
        m = DotMap({'address': {'city': 'abc'}}, _default_factory=str)

        self.assertEqual(m.address.city, 'abc')
        self.assertEqual(m.address.zipCode, '')

    def test_default_with_dynamic_false_raises(self):
        with self.assertRaises(ValueError):
            DotMap(_default_factory=str, _dynamic=False)

    def test_default_factory_must_be_callable(self):
        with self.assertRaises(TypeError):
            DotMap(_default_factory='')

    def test_copy_preserves_default(self):
        m = DotMap({'city': 'abc'}, _default_factory=str)
        c = m.copy()

        self.assertEqual(c.city, 'abc')
        self.assertNotIn('zipCode', c)
        self.assertEqual(c.zipCode, '')

    def test_deepcopy_preserves_default(self):
        m = DotMap({'address': {'city': 'abc'}}, _default_factory=str)
        c = copy.deepcopy(m)

        self.assertEqual(c.address.city, 'abc')
        self.assertNotIn('zipCode', c)
        self.assertEqual(c.zipCode, '')
        self.assertEqual(c.address.zipCode, '')

    def test_default_list(self):
        m = DotMap({}, _default_factory=list)
        self.assertEqual(m.x, [])
        self.assertEqual(m.y, [])

        m.x.append(42)
        self.assertEqual(m.x, [42])

        self.assertEqual(m.y, [])

    def test_default_factory_returning_cached_list_shares_it(self):
        # if the factory itself returns the same cached object every call,
        # keys share it -- freshness is the factory's responsibility
        cached = []
        m = DotMap({}, _default_factory=lambda: cached)

        self.assertIs(m.x, cached)
        m.x.append(42)

        self.assertIs(m.y, cached)
        self.assertEqual(m.y, [42])


class TestRecursive(unittest.TestCase):
    def test(self):
        m = DotMap()
        m.a = 5
        m_id = id(m)
        m.recursive = m
        self.assertEqual(id(m.recursive.recursive.recursive), m_id)
        outStr = str(m)
        self.assertIn('''a=5''', outStr)
        self.assertIn('''recursive=DotMap(...)''', outStr)
        d = m.toDict()
        d_id = id(d)
        d['a'] = 5
        d['recursive'] = d
        d['recursive']['recursive']['recursive']
        self.assertEqual(id(d['recursive']['recursive']['recursive']), d_id)
        outStr = str(d)
        self.assertIn(''''a': 5''', outStr)
        self.assertIn('''recursive': {...}''', outStr)
        m2 = DotMap(d)
        m2_id = id(m2)
        self.assertEqual(id(m2.recursive.recursive.recursive), m2_id)
        outStr2 = str(m2)
        self.assertIn('''a=5''', outStr2)
        self.assertIn('''recursive=DotMap(...)''', outStr2)


class Testkwarg(unittest.TestCase):
    def test(self):
        a = {'1': 'a', '2': 'b'}
        b = DotMap(a, _dynamic=False)

        def capture(**kwargs):
            return kwargs
        self.assertEqual(a, capture(**b.toDict()))


class TestDeepCopy(unittest.TestCase):
    def test(self):
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


class TestDotMapTupleToDict(unittest.TestCase):
    def test(self):
        m = DotMap({'a': 1, 'b': (11, 22, DotMap({'c': 3}))})
        d = m.toDict()
        self.assertEqual(d, {'a': 1, 'b': (11, 22, {'c': 3})})


class TestOrderedDictInit(unittest.TestCase):
    def test(self):
        o = OrderedDict([('a', 1), ('b', 2), ('c', [OrderedDict([('d', 3)])])])
        m = DotMap(o)
        self.assertIsInstance(m, DotMap)
        self.assertIsInstance(m.c[0], DotMap)


class TestFormatting(unittest.TestCase):
    def test_values_preserve_order(self):
        m = DotMap()
        m.alpha = 1
        m.bravo = 2
        m.charlie = 3

        self.assertEqual(list(m.values()), [1, 2, 3])

    def test_pprint_outputs_plain_dict(self):
        m = DotMap({'a': 1, 'sub': {'b': 2}})
        buf = StringIO()

        with redirect_stdout(buf):
            m.pprint()

        self.assertEqual(buf.getvalue(), "{'a': 1, 'sub': {'b': 2}}\n")


class TestEmptyAdd(unittest.TestCase):
    def test_base(self):
        m = DotMap()
        for i in range(7):
            m.counter += 1
        self.assertNotIsInstance(m.counter, DotMap)
        self.assertIsInstance(m.counter, int)
        self.assertEqual(m.counter, 7)

    def test_various(self):
        m = DotMap()
        m.a.label = 'test'
        m.a.counter += 2
        self.assertIsInstance(m.a, DotMap)
        self.assertEqual(m.a.label, 'test')
        self.assertNotIsInstance(m.a.counter, DotMap)
        self.assertIsInstance(m.a.counter, int)
        self.assertEqual(m.a.counter, 2)
        m.a.counter += 1
        self.assertEqual(m.a.counter, 3)

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
        m2 = DotMap() + "I'll replace that DotMap"
        self.assertEqual(m2, "I'll replace that DotMap")

    def test_protected_hierarchy(self):
        m = DotMap()
        m.protected_parent.key = 'value'

        def protectedFromAddition():
            m.protected_parent += 1
        self.assertRaises(TypeError, protectedFromAddition)

    def test_type_error_raised(self):
        m = DotMap()

        def badAddition():
            m.a += 1
            m.a += ' and tigers'
        self.assertRaises(TypeError, badAddition)


class TestMethodMasking(unittest.TestCase):
    def test_prevent_method_masking_rejects_reserved_keys(self):
        with self.assertRaises(KeyError):
            DotMap(a=1, get='mango', _prevent_method_masking=True)

        with self.assertRaises(KeyError):
            DotMap((('a', 1), ('get', 'mango')), _prevent_method_masking=True)

        with self.assertRaises(KeyError):
            DotMap({'a': 1, 'get': 'mango'}, _prevent_method_masking=True)

        with self.assertRaises(KeyError):
            DotMap({'a': 1, 'b': {'get': 'mango'}}, _prevent_method_masking=True)

    def test_dynamic_key_is_not_reserved(self):
        m = DotMap({'a': 1, '_dynamic': 2}, _prevent_method_masking=True)
        self.assertEqual(m.a, 1)
        self.assertEqual(m['_dynamic'], 2)


# Test classes for SubclassTestCase below

# class that overrides __getitem__
class MyDotMap(DotMap):
    def __getitem__(self, k):
        return super(MyDotMap, self).__getitem__(k)


# subclass with existing property
class PropertyDotMap(MyDotMap):
    def __init__(self, *args, **kwargs):
        super(MyDotMap, self).__init__(*args, **kwargs)
        self._myprop = None

    @property
    def my_prop(self):
        if not self._myprop:
            self._myprop = PropertyDotMap({'nested_prop': 123})
        return self._myprop


class SubclassTestCase(unittest.TestCase):
    def test_nested_subclass(self):
        my = MyDotMap()
        my.x.y.z = 123
        self.assertEqual(my.x.y.z, 123)
        self.assertIsInstance(my.x, MyDotMap)
        self.assertIsInstance(my.x.y, MyDotMap)

    def test_subclass_with_property(self):
        p = PropertyDotMap()
        self.assertIsInstance(p.my_prop, PropertyDotMap)
        self.assertEqual(p.my_prop.nested_prop, 123)
        p.my_prop.second.third = 456
        self.assertIsInstance(p.my_prop.second, PropertyDotMap)
        self.assertEqual(p.my_prop.second.third, 456)


class TestStaticDotMap(unittest.TestCase):
    def test_is_dotmap_subclass(self):
        m = StaticDotMap()
        self.assertIsInstance(m, StaticDotMap)
        self.assertIsInstance(m, DotMap)

    def test_empty_init(self):
        m = StaticDotMap()
        self.assertEqual(len(m), 0)
        self.assertTrue(m.empty())
        with self.assertRaises(AttributeError):
            m.missing

    def test_kwargs_init(self):
        m = StaticDotMap(a=1, b=2)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        with self.assertRaises(AttributeError):
            m.missing

    def test_dict_init(self):
        d = {'a': 1, 'b': 2, 'sub': {'c': 3, 'd': 4}}
        m = StaticDotMap(d)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        self.assertEqual(m.sub.c, 3)
        self.assertEqual(m.sub.d, 4)

    def test_missing_attribute_raises(self):
        m = StaticDotMap(a=1)
        with self.assertRaises(AttributeError):
            m.missing

    def test_missing_item_raises(self):
        m = StaticDotMap(a=1)
        with self.assertRaises(KeyError):
            m['missing']

    def test_nested_missing_attribute_raises(self):
        m = StaticDotMap({'sub': {'a': 1}})
        with self.assertRaises(AttributeError):
            m.sub.missing

    def test_dynamic_true_kwarg_raises(self):
        # StaticDotMap accepts an explicit false value but not dynamic mode.
        with self.assertRaisesRegex(ValueError, '^can not set `_dynamic=True` for StaticDotMap$'):
            StaticDotMap({'a': 1}, _dynamic=True)
        m = StaticDotMap({'a': 1}, _dynamic=False)
        self.assertFalse(m._dynamic)

    def test_nested_dicts_become_static(self):
        m = StaticDotMap({'a': 1, 'sub': {'b': 2, 'deep': {'c': 3}}})
        self.assertIsInstance(m.sub, StaticDotMap)
        self.assertIsInstance(m.sub.deep, StaticDotMap)
        with self.assertRaises(AttributeError):
            m.sub.missing
        with self.assertRaises(AttributeError):
            m.sub.deep.missing

    def test_list_of_dicts_become_static(self):
        m = StaticDotMap({
            'children': [{'name': 'a'}, {'name': 'b'}],
        })
        self.assertEqual(len(m.children), 2)
        for child in m.children:
            self.assertIsInstance(child, StaticDotMap)
            with self.assertRaises(AttributeError):
                child.missing

    def test_assignment_to_existing_or_new_key_works(self):
        # Static only disables auto-creation on read; assignment is still allowed.
        m = StaticDotMap({'a': 1})
        m.a = 10
        self.assertEqual(m.a, 10)
        m.b = 2
        self.assertEqual(m.b, 2)
        m['c'] = 3
        self.assertEqual(m['c'], 3)

    def test_dict_protocol(self):
        m = StaticDotMap({'a': 1, 'b': 2})
        self.assertEqual(set(m.keys()), {'a', 'b'})
        self.assertEqual(set(m.values()), {1, 2})
        self.assertEqual(dict(m.items()), {'a': 1, 'b': 2})
        self.assertEqual(len(m), 2)
        self.assertIn('a', m)
        self.assertNotIn('missing', m)
        self.assertEqual(m.get('a'), 1)
        self.assertEqual(m.get('missing', 'default'), 'default')

    def test_toDict_returns_plain_dict(self):
        m = StaticDotMap({'a': 1, 'sub': {'b': 2}})
        d = m.toDict()
        self.assertIsInstance(d, dict)
        self.assertNotIsInstance(d, DotMap)
        self.assertIsInstance(d['sub'], dict)
        self.assertNotIsInstance(d['sub'], DotMap)
        self.assertEqual(d, {'a': 1, 'sub': {'b': 2}})

    def test_copy_preserves_type_and_static(self):
        m = StaticDotMap({'a': 1, 'sub': {'b': 2}})
        c = m.copy()
        self.assertIsInstance(c, StaticDotMap)
        self.assertIsInstance(c.sub, StaticDotMap)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.sub.b, 2)
        with self.assertRaises(AttributeError):
            c.missing
        with self.assertRaises(AttributeError):
            c.sub.missing

    def test_deepcopy_preserves_type_and_static(self):
        m = StaticDotMap({'a': 1, 'sub': {'b': 2}})
        c = copy.deepcopy(m)
        self.assertIsInstance(c, StaticDotMap)
        self.assertIsInstance(c.sub, StaticDotMap)
        with self.assertRaises(AttributeError):
            c.missing
        with self.assertRaises(AttributeError):
            c.sub.missing

    def test_pickle_preserves_type_and_static(self):
        m = StaticDotMap({'a': 1, 'sub': {'b': 2}})
        restored = pickle.loads(pickle.dumps(m))
        self.assertIsInstance(restored, StaticDotMap)
        self.assertIsInstance(restored.sub, StaticDotMap)
        self.assertEqual(restored.a, 1)
        self.assertEqual(restored.sub.b, 2)
        with self.assertRaises(AttributeError):
            restored.missing
        with self.assertRaises(AttributeError):
            restored.sub.missing

    def test_init_from_dotmap(self):
        source = DotMap({'a': 1, 'sub': {'b': 2}})
        m = StaticDotMap(source)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.sub.b, 2)
        with self.assertRaises(AttributeError):
            m.missing

    def test_equality_with_dict_and_dotmap(self):
        m = StaticDotMap({'a': 1, 'b': 2})
        self.assertEqual(m, {'a': 1, 'b': 2})
        self.assertEqual(m, DotMap({'a': 1, 'b': 2}))
        self.assertEqual(m, StaticDotMap({'a': 1, 'b': 2}))

    def test_prevent_method_masking_still_works(self):
        # The flag introduced for DotMap should pass through to StaticDotMap.
        with self.assertRaises(KeyError):
            StaticDotMap(a=1, get='mango', _prevent_method_masking=True)
        with self.assertRaises(KeyError):
            StaticDotMap({'a': 1, 'get': 'mango'}, _prevent_method_masking=True)


class TestKeyConvertHook(unittest.TestCase):
    def fix_illegal_key(self, key):
        return key.replace(".", "_").replace("-","_")
    
    def test(self):
        # by default key_convert_hook = None
        d = DotMap({"dot.map":123}, _dynamic=False)
        self.assertRaises(AttributeError, lambda: d.dot.map)
        
        # replace @ with _ 
        d = DotMap({"dot@map":"dot_map"}, _key_convert_hook = lambda k: k.replace('@','_'))
        self.assertEqual(d.dot_map, "dot_map")
        
        # replace multiple keys, apply to nested fields
        d = DotMap({"dot@map":{"dot!map":"dot_map"}}, _key_convert_hook = lambda k: k.replace('@','_').replace('!','_'))
        self.assertEqual(d.dot_map.dot_map, "dot_map")

        # replace multiple keys with a _key_convert_hook function
        d = DotMap({"dot-map":123}, _key_convert_hook = self.fix_illegal_key)
        self.assertEqual(d.dot_map, 123)
        
        # replace the entire key with another one
        d = DotMap({"dot!map":456}, _key_convert_hook = lambda k: 'DOTMAP' if k == 'dot!map' else k)
        self.assertEqual(d.DOTMAP, 456)


class TestInitFromDotMap(unittest.TestCase):
    def test_nested_dotmaps_are_copied(self):
        source = DotMap({'a': 1, 'sub': {'b': 2}})
        copied = DotMap(source)

        self.assertEqual(copied.a, 1)
        self.assertEqual(copied.sub.b, 2)
        self.assertIsNot(copied, source)
        self.assertIsNot(copied.sub, source.sub)
