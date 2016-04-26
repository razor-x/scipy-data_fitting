from setuptools import find_packages, setup

from scipy_data_fitting import __version__

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='scipy-data_fitting',
    version=__version__,
    author='Evan Sosenko',
    author_email='razorx@evansosenko.com',
    packages=find_packages(exclude=['docs']),
    url='https://github.com/razor-x/scipy-data_fitting',
    license='MIT',
    description='Complete pipeline for easy data fitting with Python.',
    long_description=long_description,
    test_suite='nose',
    install_requires = [
        'lmfit>=0.8.0,<0.9.0',
        'matplotlib',
        'numpy',
        'scipy',
        'sympy'
    ],
    tests_require = [
        'nose'
    ]
)
