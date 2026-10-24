import unittest

from dotmap import DotMap


class TestDynamicMethodMasking(unittest.TestCase):
    def test_dynamic_descendants_preserve_masking_guard(self):
        for access in ('attribute', 'item'):
            mapping = DotMap(_prevent_method_masking=True)
            child = mapping.child if access == 'attribute' else mapping['child']
            for descendant in (child, child.grandchild):
                with self.subTest(access=access, depth=descendant is child):
                    self.assertTrue(descendant._prevent_method_masking)
                    with self.assertRaises(KeyError):
                        descendant.get = 'masked'
                    self.assertNotIn('get', descendant)
                    descendant.value = 1
                    self.assertEqual(descendant.value, 1)

    def test_prepopulated_and_dynamic_children_match(self):
        mapping = DotMap({'existing': {}}, _prevent_method_masking=True)
        for child in (mapping.existing, mapping.created):
            with self.subTest(existing=child is mapping.existing):
                with self.assertRaises(KeyError):
                    child.items = 'masked'
                self.assertEqual(list(child.items()), [])

    def test_default_dynamic_children_still_allow_method_keys(self):
        mapping = DotMap()
        mapping.child.get = 'allowed'
        self.assertEqual(mapping.child['get'], 'allowed')
        self.assertFalse(mapping.child._prevent_method_masking)

    def test_default_factory_remains_in_charge(self):
        child = DotMap()
        mapping = DotMap(_prevent_method_masking=True, _default_factory=lambda: child)
        self.assertIs(mapping.child, child)
        self.assertFalse(child._prevent_method_masking)


class GuardedNoArgumentMap(DotMap):
    def __init__(self):
        super().__init__(_prevent_method_masking=True)


class TestDynamicMaskingSubclass(unittest.TestCase):
    def test_no_argument_subclass_constructor_still_works(self):
        mapping = GuardedNoArgumentMap()
        child = mapping.child
        self.assertIsInstance(child, GuardedNoArgumentMap)
        with self.assertRaises(KeyError):
            child.get = 'masked'
