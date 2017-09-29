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
    version='1.0.0',
    packages=['sd_utils'],
    license='(c) 2017 StratoDem Analytics. All rights reserved.',
    description='StratoDem utilities',
    long_description='General logging and QoL utilities',
    author='StratoDem Analytics',
    author_email='tech@stratodem.com',
    url='https://github.com/StratoDem/SDUtils',
    install_requires=[
        'slackclient',
        'numpy',
        'pandas',
        'joblib',
        'dask',
        'xarray',
        'geopandas',
        'simpledbf',
        'pyarrow',
    ],
)
