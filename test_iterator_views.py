import unittest

from dotmap import DotMap


class IteratorViewTests(unittest.TestCase):
    def test_iterkeys_and_itervalues(self):
        mapping = DotMap(a=1, b=2)
        self.assertEqual(list(mapping.iterkeys()), ['a', 'b'])
        self.assertEqual(list(mapping.itervalues()), [1, 2])
        keys = mapping.iterkeys()
        self.assertIs(iter(keys), keys)

    def test_mapping_views_are_live(self):
        mapping = DotMap(a=1)
        keys = mapping.viewkeys()
        values = mapping.viewvalues()
        items = mapping.viewitems()
        mapping['b'] = 2
        self.assertEqual(list(keys), ['a', 'b'])
        self.assertEqual(list(values), [1, 2])
        self.assertEqual(list(items), [('a', 1), ('b', 2)])
