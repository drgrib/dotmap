========
DotMap
========

DotMap is a dot-access dictionary that

* is dynamically expandable
* can be initialized with keys
* easily initializes from :code:`dict`
* easily converts to :code:`dict`
* is ordered by insertion

.. code-block:: python
	
	from dotmap import DotMap	

	m = DotMap()
	
	# new sub maps are created dynamically
	m.people.john.age = 32
	m.people.john.job = 'programmer'
	m.people.mary.age = 24
	m.people.mary.job = 'designer'

	# iteration ordered by insertion
	for k, v in m.people.items():
		print k, v
	print

	# key initialization
	m = DotMap(a=1, b=2)

	# easy conversion to dictionary
	d = m.toDict()

	# easy initialization from dictionary
	newMap = DotMap(d)
	print newMap

	# built-in pprint
	newMap.pprint()
