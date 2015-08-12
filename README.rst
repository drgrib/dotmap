========
DotMap
========

DotMap is a dot-access dictionary that is

* ordered by insertion
* dynamically expandable
::

	from dotmap import DotMap
	d = DotMap()
	d.city.name = 'SF'
	d.city.state = 'CA'
	d.pprint()