import unittest

from dotmap import DotMap


class TestMappingHelpers(unittest.TestCase):
    def test_dir_filters_nonstring_keys_without_modifying_data(self):
        mapping = DotMap({1: 'one', 'name': 'value', None: 'none'})
        assert dir(mapping) == ['name']
        assert list(mapping.items()) == [(1, 'one'), ('name', 'value'), (None, 'none')]


    def test_dir_remains_sorted_and_handles_empty_maps(self):
        assert dir(DotMap(z=1, a=2)) == ['a', 'z']
        assert dir(DotMap()) == []
