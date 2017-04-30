#!/usr/bin/env python
# coding:utf-8
from setuptools import setup
from MicroCore import (
    __title__, __version__, __author__, __url__,
    __author_email__, __license__)
setup(
    name=__title__,
    version=__version__,
    description="MicroCore is an HTTP library",
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    package_dir={'MicroCore': 'microcore'},
    packages=['MicroCore'],
    include_package_data=True,
    keywords='http',
)


