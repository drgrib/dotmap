import unittest
from dotmap import DotMap


class DotMapTestCase(unittest.TestCase):

	def _get_dict(self):
		return {
			'a':1,
			'b':2,
			'subD': {'c':3, 'd':4}
		}

	def test_init(self):
		d = DotMap(self._get_dict())
		self.assertEqual(len(d), 3)

	def test_copy(self):
		d = DotMap(self._get_dict())
		c = d.copy()
		self.assertEqual(d,c)

	def test_del(self):
		am = DotMap()
		am.some.deep.path.cuz.we = 'can'
		del am.some.deep
		self.assertEqual(len(am), 1)

if __name__ == '__main__':
    unittest.main()

a = """	
	print(OrderedDict.fromkeys([1,2,3]))
	print(DotMap.fromkeys([1,2,3], 'a'))
	print(dd.get('a'))
	print(dd.get('f',33))
	print(dd.get('f'))
	print(dd.has_key('a'))
	dd.update([('rat',5),('bum',4)], dog=7,cat=9)
	dd.update({'lol':1,'ba':2})
	print(dd)
	print
	for k in dd:
		print(k)
	print('a' in dd)
	print('c' in dd)
	dd.c.a = 1
	print(dd.toDict())
	dd.pprint()
	print
	print(dd.values())
	dm = DotMap(name='Steve', job='programmer')
	print(dm)
	print(issubclass(dm.__class__, dict))
	
"""