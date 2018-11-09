#!/usr/bin/env bash

. venv/bin/activate

python setup.py bdist_wheel --universal
python setup.py bdist_wheel
python setup.py bdist_egg
python setup.py sdist
