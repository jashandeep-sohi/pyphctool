#!/usr/bin/env python

from distutils.core import setup

setup(name='pyphctool',
      version='0.1',
      description='A Python tool for finding and setting PHC VIDs.',
      author='Jashandeep Sohi',
      author_email='jashandeep.s.sohi@gmail.com',
      url='https://github.com/jashandeep-sohi/pyphctool',
      license='gplv3',
      py_modules = ['pyphctoolcore'],
      scripts = ['pyphctool'],
      data_files = [('/etc/phc', ['vids.conf'])]
     )

