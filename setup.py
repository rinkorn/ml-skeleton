#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='titanic',
      version='1.0',
      description='ML repo skeleton',
      package_dir={"": "src"},
      packages=find_packages(where="src"),
     )
