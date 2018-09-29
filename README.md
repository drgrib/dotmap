# DotMap

`DotMap` is a dot-access `dict` subclass that
* has dynamic hierarchy creation
* can be initialized with keys
* easily initializes from :code:`dict`
* easily converts to :code:`dict`
* is ordered by insertion

The key feature is exactly what you want: dot-access

``` python
from dotmap import DotMap
m = DotMap()
m.name = 'Joe'
print 'Hello ' + m.name
# Hello Joe
```

However, `DotMap` is a `dict` and you can treat it like a :code:`dict` as needed

``` python
print m['name']
# Joe
m.name += ' Smith'
m['name'] += ' Jr'
print m.name
# Joe Smith Jr
```

It also has fast, automatic hierarchy (which can be deactivated by initializing with `DotMap(_dynamic=False)`)

``` python
m = DotMap()
m.people.steve.age = 31
```

And key initialization

``` python
m = DotMap(a=1, b=2)
```

You can initialize it from :code:`dict` and convert it to `dict`

``` python
d = {'a':1, 'b':2}

m = DotMap(d)
print m
# DotMap(a=1, b=2)

print m.toDict()
# {'a': 1, 'b': 2}
```

And it has iteration that is ordered by insertion

``` python
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
```

There is also built-in `pprint` as `dict` or `json` for debugging a large `DotMap`

``` python
m.pprint()
# {'people': {'dave': {'age': 55, 'job': 'manager'},
#             'john': {'age': 32, 'job': 'programmer'},
#             'mary': {'age': 24, 'job': 'designer'}}}
m.pprint(pformat='json')
# {
#     "people": {
#         "dave": {
#	      "age": 55,
#	      "job": "manager"
# 	  },
# 	  "john": {
#	      "age": 32,
#	      "job": "programmer"
# 	  },
# 	  "mary": {
#	      "age": 24,
#	      "job": "designer"
# 	  }
#     }
# }
```

And many other features involving dots and dictionaries that will be immediately intuitive when used.