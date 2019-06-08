#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="openfootprint",
    version="0.0.1",
    description="Open source software for managing ecological footprint, including carbon emissions.",
    long_description=open("README.md").read(),
    author="Openfootprint",
    author_email="contact@openfootprint.org",
    url="https://github.com/openfootprint/openfootprint",
    packages=[],
    license="Apache 2.0",
    platforms="any",
    zip_safe=False,
)