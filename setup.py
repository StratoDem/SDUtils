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
    version='1.1.0',
    packages=['sd_utils'],
    license='(c) 2017 StratoDem Analytics. All rights reserved.',
    description='StratoDem utilities',
    long_description='General logging and QoL utilities',
    author='StratoDem Analytics',
    author_email='tech@stratodem.com',
    url='https://github.com/StratoDem/SDUtils',
    install_requires=[
        'slackclient',
        'numpy>=1.13.3',
        'pandas>=0.21.1',
        'joblib',
        'dask>=0.16.0',
        'xarray',
        'geopandas>=0.3.0',
        'simpledbf',
        'pyarrow>=0.7.1',
        'toolz',
        'cloudpickle',
    ],
)
