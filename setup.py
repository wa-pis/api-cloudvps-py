#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.version_info < (2, 5):
    raise NotImplementedError(
        "Sorry, you need at least Python 2.5 or \
        Python 3.x to use api-cloudvps-py.")

with open('README.rst') as f:
    readme = f.read()


setup(name='api-cloudvps-py',
      version='0.1.0',
      description=readme,
      url='https://github.com/wa-pis/api-cloudvps-py',
      author='Anton Grudin',
      author_email='onepis2word@gmail.com',
      license='MIT',
      packages=['cloudvps', 'cloudvps/objects'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Topic :: Internet :: WWW/HTTP',
          'Natural Language :: Russian',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='api-client api python requests reg.ru',
      install_requires=[
          'requests',
          'future',
      ],
      test_suite='tests',
      zip_safe=False)
