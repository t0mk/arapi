#!/usr/bin/env python

#http://bugs.python.org/issue15881#msg170215
import multiprocessing

from setuptools import setup

setup(name='arapi',
      version='0.1',
      description='REST API to Augeas tree',
      author='Tomas Karasek`',
      author_email='tom.to.the.k@gmail.com',
      url='https://github.com/t0mk/arapi',
      packages=['arapi'],
      package_data={'arapi': ['conf/*']},
      scripts=['arapid'],
      test_suite='nose.collector',
      tests_require='nose',
     )
