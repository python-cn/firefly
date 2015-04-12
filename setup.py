# coding=utf-8
import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    install_requires = [p.strip() for p in f.readlines()]

setup(
    name='pythoncn',
    description='A social forum for pythonista',
    url='https://github.com/python-cn/firefly',
    version='0.1.0',

    author='Python-cn Team',
    author_email='ciici123@gmail.com',

    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('.', exclude=('tests*')),
    install_requires=install_requires,
)
