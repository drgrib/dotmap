import unittest

from dotmap import DotMap


class TestMappingHelpers(unittest.TestCase):
    def test_move_to_end_uses_visible_items(self):
        mapping = DotMap(a=1, b=2, c=3)
        assert mapping.move_to_end('a') is None
        assert list(mapping) == ['b', 'c', 'a']
        mapping.move_to_end('a', last=False)
        assert list(mapping) == ['a', 'b', 'c']
        with self.assertRaises(KeyError):
            mapping.move_to_end('missing')
        assert list(mapping) == ['a', 'b', 'c']


    def test_reverse_tracks_order_and_mutations(self):
        mapping = DotMap(a=1, b=2)
        assert list(reversed(mapping)) == ['b', 'a']
        mapping['c'] = 3
        assert list(reversed(mapping)) == ['c', 'b', 'a']
        assert list(reversed(DotMap())) == []


    def test_popitem_can_remove_the_first_item(self):
        mapping = DotMap(a=1, b=2)
        assert mapping.popitem(last=False) == ('a', 1)
        assert mapping.popitem() == ('b', 2)
        with self.assertRaises(KeyError):
            mapping.popitem(last=False)
