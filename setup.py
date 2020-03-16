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
    version='2.5.0',
    packages=['sd_utils'],
    license='(c) 2017- StratoDem Analytics. All rights reserved.',
    description='StratoDem utilities',
    long_description='General logging and QoL utilities',
    author='StratoDem Analytics',
    author_email='tech@stratodem.com',
    url='https://github.com/StratoDem/SDUtils',
    install_requires=[
        'slackclient==2.5.0',
        'numpy==1.18.1',
        'pandas==1.0.2',
        'joblib',
        'dask==2.12.0',
        'xarray>=0.10.0',
        'geopandas>=0.3.0',
        'simpledbf>=0.2.6',
        'python-snappy',
        'pyarrow==0.16.0',
        'toolz',
        'cloudpickle',
        'fastparquet',
    ],
)
