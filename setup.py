from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	version = '1.3.21',
    name='dotmap',
    packages=['dotmap'],  # this must be the same as the name above
    description='ordered, dynamically-expandable dot-access dictionary',
    author='Chris Redford',
    author_email='credford@gmail.com',
    url='https://github.com/drgrib/dotmap',  # use the URL to the github repo
    download_url='https://github.com/drgrib/dotmap/tarball/1.0',
    keywords=['dict', 'dot', 'map', 'order', 'ordered',
              'ordereddict', 'access', 'dynamic'],  # arbitrary keywords
    classifiers=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
