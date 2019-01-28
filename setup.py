"""
StratoDem Analytics : setup.py
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

September 29, 2017
"""
from setuptools import setup


setup(
    name='SDUtils',
    version='2.1.0',
    packages=['sd_utils'],
    license='(c) 2017- StratoDem Analytics. All rights reserved.',
    description='StratoDem utilities',
    long_description='General logging and QoL utilities',
    author='StratoDem Analytics',
    author_email='tech@stratodem.com',
    url='https://github.com/StratoDem/SDUtils',
    install_requires=[
        'slackclient>=1.1.0',
        'numpy>=1.16.0',
        'pandas>=0.24',
        'joblib',
        'dask>=1.1.0',
        'xarray>=0.10.0',
        'geopandas>=0.3.0',
        'simpledbf>=0.2.6',
        'pyarrow==0.12',
        'toolz',
        'cloudpickle',
    ],
)
