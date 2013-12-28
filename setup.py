#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='pycis',
      version='0.0.1-dev',
      license='MIT',
      description='Subtitles, faster than your thoughts',
      long_description=open('README.md').read(),
      keywords='stream video movie episode tv show film',
      url='https://github.com/marcwebbie/pycis',
      author='Marcwebbie',
      author_email='marcwebbie@gmail.com',
      scripts=["bin/pycis-cli"],
      packages=find_packages(),
      classifiers=['Development Status :: Alpha',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Multimedia :: Video'],
      install_requires=open('requirements.pip').readlines(),
      test_suite='tests.test')
