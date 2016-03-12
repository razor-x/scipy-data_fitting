from setuptools import setup
import os
import subprocess
import tempfile

description = 'Data fitting system with SciPy.'
long_description = description

try:
    pandoc = subprocess.check_output(
        ['which', 'pandoc'],
        stderr=subprocess.STDOUT,
        universal_newlines=True)
except subprocess.CalledProcessError:
    pandoc = None

if pandoc and os.path.exists('README.md'):
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, 'README.md')

    with open(temp_path, 'a') as f:
        for line in open('README.md', 'r'):
            # Remove lines that match Markdown images,
            # they are not supported in `long_description`.
            if not line.startswith('!['): f.write(line)

    os.system('pandoc -s ' + temp_path + ' -t rst -o README.txt')
    long_description = open('README.txt').read()
    os.remove(temp_path)
    os.rmdir(temp_dir)

setup(
    name = 'scipy-data_fitting',
    version = '0.2.5',
    author = 'Evan Sosenko',
    author_email = 'razorx@evansosenko.com',
    packages = ['scipy_data_fitting', 'scipy_data_fitting/figure'],
    url = 'https://github.com/razor-x/scipy-data_fitting',
    license = 'MIT License, see LICENSE.txt',
    description = description,
    long_description = long_description,
    install_requires = [
        'lmfit>=0.8.0,<0.9.0',
        'matplotlib',
        'numpy',
        'scipy',
        'sympy',
    ],
    tests_require = [
        'nose',
    ],
)
