#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst") as readme_file:
    long_description = readme_file.read()

setup(
    name="openfootprint",
    version="0.0.1",
    description="Open source software for managing ecological footprint, including carbon emissions.",
    long_description=open("README.md").read(),
    author="Openfootprint",
    author_email="",
    url="https://github.com/openfootprint/openfootprint",
    packages=[],
    license="Apache 2.0",
    platforms='any',
    zip_safe=False
)