from collections import OrderedDict
from pprint import pprint

class DotMap(object):
	def __init__(self, *args, **kwargs):
		self._map = OrderedDict()
		if args:
			d = args[0]
			if type(d) is dict:
				for k,v in d.iteritems():
					if type(v) is dict:
						v = DotMap(v)
					self._map[k] = v
		if kwargs:
			for k,v in kwargs.iteritems():
				self._map[k] = v

	def items(self):
		return self.iteritems()

	def iteritems(self):
		return self._map.iteritems()

	def __iter__(self):
		return self._map.__iter__()

	def next(self):
		return self._map.next()

	def __setitem__(self, k, v):
		self._map[k] = v
	def __getitem__(self, k):
		if k not in self._map:
			# automatically extend to new DotMap
			self[k] = DotMap()
		return self._map[k]

	def __setattr__(self, k, v):
		if k == '_map':
			super(DotMap, self).__setattr__(k,v)
		else:
			self[k] = v

	def __getattr__(self, k):
		if k == '_map':
			super(DotMap, self).__getattr__(k)
		else:
			return self[k]

	def __contains__(self, k):
		return self._map.__contains__(k)

	def __str__(self):
		items = []
		for k,v in self._map.iteritems():
			items.append('{}={}'.format(k, v))
		out = 'DotMap({})'.format(', '.join(items))
		return out

	def toDict(self):
		d = {}
		for k,v in self.items():
			if type(v) is DotMap:
				v = v.toDict()
			d[k] = v
		return d

	def pprint(self):
		pprint(self.toDict())

