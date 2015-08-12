========
DotMap
========

DotMap is a dot-access dictionary that

* is dynamically expandable
* can be initialized with keys
* easily initializes from `dict`
* easily converts to `dict`
* subclasses `OrderedDict` which
** is ordered by insertion
** subclasses `dict`

.. highlight:: python
	
	m = DotMap()

	# key initialization
	
	# new sub maps are created dynamically
	m.people.john.age = 32
	m.people.john.job = 'programmer'
	m.people.mary.age = 24
	m.people.mary.job = 'designer'

	# iteration ordered by insertion
	for k, v in m.people.items():
		print k, v
	print

	# easy conversion to dictionary
	d = m.toDict()

	# easy initialization from dictionary
	newMap = DotMap(d)
	print newMap

	# built-in pprint
	newMap.pprint()
