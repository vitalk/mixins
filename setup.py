#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from os.path import join, dirname
from setuptools import setup


version = re.search("__version__ = '([^']+)'",
                    open(join(dirname(__file__), 'mixins.py')).read()).group(1)


setup(name='mixins',
      author='Vital Kudzelka',
      author_email='vital.kudzelka@gmail.com',
      version=version
      description='A python module that contains a some useful mixins.',
)
