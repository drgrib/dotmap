from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='dotmap',
      version=version,
      description="ordered, dynamically-expandable dot-access dictionary",
      long_description="""\
ordered, dynamically-expandable dot-access dictionary""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='dict dot map order ordered ordereddict access dynamic',
      author='Chris Redford',
      author_email='credford@gmail.com',
      url='https://github.com/drgrib/dotmap',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collections',
          'pprint'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
