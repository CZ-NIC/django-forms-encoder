#!/usr/bin/python3
"""Setup script for django-forms-encoder."""
import os
from distutils.command.build import build

from setuptools import find_packages, setup


def readme():
    """Return content of README file."""
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        return f.read()


INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
EXTRAS_REQUIRE = {'quality': ['isort', 'flake8', 'pydocstyle', 'mypy']}
VERSION = '0.2'


setup(name='django_forms_encoder',
      version=VERSION,
      description='Encode django forms to JSON',
      long_description=readme(),
      author='Jan Musílek',
      author_email='jan.musilek@nic.cz',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      zip_safe=False,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
      ])
