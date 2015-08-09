#!/bin/bash

# Exit on error
set -e

flake8 dockermon.py test_dockermon.py
nosetests -vd $@
