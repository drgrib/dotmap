========
DotMap
========

:code:`DotMap` is a dot-access :code:`dict` subclass that

* has dynamic child creation
* can be initialized with keys
* easily initializes from :code:`dict`
* easily converts to :code:`dict`
* is ordered by insertion

The key feature is exactly what you want: dot-access

.. code-block:: python

	from dotmap import DotMap
	m = DotMap()
	m.name = 'Joe'
	print 'Hello ' + m.name
	# Hello Joe

However, :code:`DotMap` is a :code:`dict` and you can treat it like a :code:`dict` as needed

.. code-block:: python

	print m['name']
	# Joe
	m.name += ' Smith'
	m['name'] += ' Jr'
	print m.name
	# Joe Smith Jr

It also has fast, automatic hierarchy (which can be deactivated by initializing with :code:`DotMap(_dynamic=False)`)

.. code-block:: python

	m = DotMap()
	m.people.steve.age = 31

And key initialization

.. code-block:: python

	m = DotMap(a=1, b=2)

You can initialize it from :code:`dict` and convert it to :code:`dict`

.. code-block:: python

	d = {'a':1, 'b':2}
	
	m = DotMap(d)
	print m
	# DotMap(a=1, b=2)
	
	print m.toDict()
	# {'a': 1, 'b': 2}

And it has iteration that is ordered by insertion

.. code-block:: python

	m = DotMap()

	m.people.john.age = 32
	m.people.john.job = 'programmer'
	m.people.mary.age = 24
	m.people.mary.job = 'designer'
	m.people.dave.age = 55
	m.people.dave.job = 'manager'

	for k, v in m.people.items():
		print k, v
	print

	# john DotMap(age=32, job='programmer')
	# mary DotMap(age=24, job='designer')
	# dave DotMap(age=55, job='manager')	

There is also built-in :code:`pprint` as :code:`dict` for debugging a large :code:`DotMap`

.. code-block:: python

	m.pprint()
	# {'people': {'dave': {'age': 55, 'job': 'manager'},
	#             'john': {'age': 32, 'job': 'programmer'},
	#             'mary': {'age': 24, 'job': 'designer'}}}

And many other features involving dots and dictionaries that will be immediately intuitive when used.