#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of breaks.
# https://github.com/fitnr/breaks

# Licensed under the GPL license:
# https://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

from setuptools import setup

try:
    readme = open('README.rst').read()
except IOError:
    readme = ''

with open('breaks/__init__.py') as i:
    version = next(r for r in i.readlines() if '__version__' in r).split('=')[1].strip('"\' \n')

setup(
    name='breaks',
    version=version,
    description='calculate bins on spatial data',
    long_description=readme,
    keywords='gis geodata chloropleth',
    author='fitnr',
    author_email='contact@fakeisthenewreal.org',
    url='https://github.com/fitnr/breaks',
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=['breaks'],
    include_package_data=False,
    install_requires=[
        'numpy >=1.10.4, <1.11',
        'scipy >=0.15.1, <0.20',
        'pysal >=1.11.0, <1.12',
        'fiona >=1.6.0, <2.0',
        'fionautil >=0.5.1, <0.6.0',
        'click >=6.2, <7',
    ],
    entry_points={
        'console_scripts': [
            'breaks=breaks.cli:main',
        ],
    },
    test_suite='tests',
)
