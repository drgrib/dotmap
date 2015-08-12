from distutils.core import setup
setup(
	name = 'dotmap',
	packages = ['dotmap'], # this must be the same as the name above
	version = '1.0',
	description = 'ordered, dynamically-expandable dot-access dictionary',
	author = 'Chris Redford',
	author_email = 'credford@gmail.com',
	url = 'https://github.com/drgrib/dotmap', # use the URL to the github repo
	download_url = 'https://github.com/drgrib/dotmap/1.0',
	keywords = ['dict', 'dot', 'map', 'order', 'ordered', 'ordereddict', 'access', 'dynamic'], # arbitrary keywords
	classifiers = [],
	install_requires=['collections','pprint'],
)