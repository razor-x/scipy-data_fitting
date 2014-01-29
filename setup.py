from setuptools import setup
import os
import subprocess

description = 'Data fitting system with SciPy.'
long_description = description

try:
    pandoc = subprocess.check_output(
        ['which', 'pandoc'],
        stderr=subprocess.STDOUT,
        universal_newlines=True)
except subprocess.CalledProcessError:
    pandoc = None

if pandoc:
    os.system('pandoc -s README.md -t rst -o README.txt')
    long_description = open('README.txt').read()

setup(
    name = 'scipy-data_fitting',
    version = '0.0.1',
    author = 'Evan Sosenko',
    author_email = 'razorx@evansosenko.com',
    packages = ['scipy_data_fitting'],
    url = 'https://github.com/razor-x/scipy-data_fitting',
    license = 'MIT License, see LICENSE.txt',
    description = description,
    long_description = long_description,
    install_requires = [
        'matplotlib',
        'numpy',
        'scipy',
        'sympy'
    ]
)
