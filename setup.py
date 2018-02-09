#!/usr/bin/env python3

import os

from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='wrant',
    version='0.1.0.dev0',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    zip_safe=True,
    include_package_data=False,
    description='Writing Assistant',
    author='Francesco Moramarco',
    license='Proprietary',
    long_description=(
        'https://github.com/fm2g11/wrant'
    ),
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers, Writers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
