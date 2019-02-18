# DotMap

[![Build Status](https://travis-ci.com/drgrib/dotmap.svg?branch=master)](https://travis-ci.com/drgrib/dotmap)

`DotMap` is a dot-access `dict` subclass that
* has dynamic hierarchy creation
* can be initialized with keys
* easily initializes from `dict`
* easily converts to `dict`
* is ordered by insertion

The key feature is exactly what you want: dot-access

``` python
from dotmap import DotMap
m = DotMap()
m.name = 'Joe'
print('Hello ' + m.name)
# Hello Joe
```

However, `DotMap` is a `dict` and you can treat it like a `dict` as needed

``` python
print(m['name'])
# Joe
m.name += ' Smith'
m['name'] += ' Jr'
print(m.name)
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

You can initialize it from `dict` and convert it to `dict`

``` python
d = {'a':1, 'b':2}

m = DotMap(d)
print(m)
# DotMap(a=1, b=2)

print(m.toDict())
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
	print(k, v)
print

# john DotMap(age=32, job='programmer')
# mary DotMap(age=24, job='designer')
# dave DotMap(age=55, job='manager')
```

It also has automatic counter initialization

``` python
m = DotMap()
for i in range(7):
	m.counter += 1
print(m.counter)
# 7
```

And automatic addition initializations of any other type

``` python
m = DotMap()
m.quote += 'lions'
m.quote += ' and tigers'
m.quote += ' and bears'
m.quote += ', oh my'
print(m.quote)
# lions and tigers and bears, oh my
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

## A note on unpacking (using the `**` operator)
Unpacking `DotMap` can be done like this
``` python
m = DotMap()
m.a = 1
simple_unpack = dict(**m.toDict())
print(simple_unpack)
# {'a': 1}
```

I've given multiple tries to getting the syntax to work with just `**m` and [it's just not worth the effort](https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict/39375731#39375731) when the workaround is this simple. If you can figure out a way to fully ace the `dict` subclass this way and still keep all the unit tests functioning, submit a PR and I'll be happy to review.