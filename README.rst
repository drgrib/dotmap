========
DotMap
========

DotMap is a dot-access dictionary that is

* ordered by insertion
* dynamically expandable
::
	
	m = DotMap()
	
	# new sub maps are created dynamically
	m.people.john.age = 32
	m.people.john.job = 'programmer'
	m.people.mary.age = 24
	m.people.mary.job = 'designer'

	# iteration ordered by insertion
	for k, v in m.people.items():
		# accessible by brackets
		print k, v
	print

	# easy conversion to dictionary
	d = m.toDict()

	# easy initialization from dictionary
	newMap = DotMap(d)
	print newMap

	# built-in pprint
	newMap.pprint()
