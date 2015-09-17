from collections import OrderedDict
from pprint import pprint
from sys import version_info
from inspect import ismethod

class DotMap(OrderedDict):

	def __init__(self, *args, **kwargs):
		self._map = OrderedDict()
		if args:
			d = args[0]
			if type(d) is dict:
				for k,v in self.__call_items(d):
					if type(v) is dict:
						v = DotMap(v)
					self._map[k] = v
		if kwargs:
			for k,v in self.__call_items(kwargs):
				self._map[k] = v

	def __call_items(self, obj):
		if hasattr(obj, 'iteritems') and ismethod(getattr(obj, 'iteritems')):
			return obj.iteritems()
		else:
			return obj.items()

	def items(self):
		return self.iteritems()

	def iteritems(self):
		return self.__call_items(self._map)

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

	def __delattr__(self, key):
		return self._map.__delitem__(key)

	def __contains__(self, k):
		return self._map.__contains__(k)

	def __str__(self):
		items = []
		for k,v in self.__call_items(self._map):
			items.append('{0}={1}'.format(k, repr(v)))
		out = 'DotMap({0})'.format(', '.join(items))
		return out

	def __repr__(self):
		return str(self)

	def toDict(self):
		d = {}
		for k,v in self.items():
			if type(v) is DotMap:
				v = v.toDict()
			d[k] = v
		return d

	def pprint(self):
		pprint(self.toDict())

	# proper dict subclassing
	def values(self):
		return self._map.values()

	@classmethod
	def parseOther(self, other):
		if type(other) is DotMap:
			return other._map
		else:
			return other	
	def __cmp__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__cmp__(other)
	def __eq__(self, other):
		other = DotMap.parseOther(other)
		if not isinstance(other, dict):
			return False
		return self._map.__eq__(other)
	def __ge__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__ge__(other)
	def __gt__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__gt__(other)
	def __le__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__le__(other)
	def __lt__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__lt__(other)
	def __ne__(self, other):
		other = DotMap.parseOther(other)
		return self._map.__ne__(other)

	def __delitem__(self, key):
		return self._map.__delitem__(key)
	def __len__(self):
		return self._map.__len__()
	def clear(self):
		self._map.clear()
	def copy(self):
		return self
	def get(self, key, default=None):
		return self._map.get(key, default)
	def has_key(self, key):
		return key in self._map
	def iterkeys(self):
		return self._map.iterkeys()
	def itervalues(self):
		return self._map.itervalues()
	def keys(self):
		return self._map.keys()
	def pop(self, key, default=None):
		return self._map.pop(key, default)
	def popitem(self):
		return self._map.popitem()
	def setdefault(self, key, default=None):
		self._map.setdefault(key, default)
	def update(self, *args, **kwargs):
		if len(args) != 0:
			self._map.update(*args)
		self._map.update(kwargs)
	def viewitems(self):
		return self._map.viewitems()
	def viewkeys(self):
		return self._map.viewkeys()
	def viewvalues(self):
		return self._map.viewvalues()
	@classmethod
	def fromkeys(cls, seq, value=None):
		d = DotMap()
		d._map = OrderedDict.fromkeys(seq, value)
		return d