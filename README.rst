.. |PyPI version| image:: https://badge.fury.io/py/api-cloudvps-py.svg
   :target: https://badge.fury.io/py/api-cloudvps-py
.. |GitHub version| image:: https://badge.fury.io/gh/wa-pis%2Fapi-cloudvps-py.svg
   :target: https://badge.fury.io/gh/wa-pis%2Fapi-cloudvps-py
.. image:: https://travis-ci.org/wa-pis/api-cloudvps-py.svg?branch=master
    :target: https://travis-ci.org/wa-pis/api-cloudvps-py

INSTALLING
==========

.. code:: bash

    $ pip install api-cloudvps-py
    # or use source code package, after extract
    $ python setup.py install

How to obtain token
===================

If you want to work with reg.ru cloudvps api client
`participate <https://www.reg.ru/company/news/9009>`__

USAGE
=====

.. code:: python

    # import
    >>> from cloudvps import Api
    >>> api = Api('3f7c0a3d*****356b45d59f71a')
    # or
    >>> import cloudvps
    >>> api = cloudvps.Api('3f7c0a3d*****356b45d59f71a')
    >>> common = api.common
    >>> print(common.sizes())
    {'sizes': [{'disk': 20, 'id': 5, 'memory': 512, 'name': 'Меркурий', 'slug': 'test_512', 'vcpus': 1, 'weight': 10}, {'disk': 30, 'id': 1, 'memory': 1024, 'name': 'Марс', 'slug': 'test', 'vcpus': 1, 'weight': 20}, {'disk': 40, 'id': 3, 'memory': 2048, 'name': 'Венера', 'slug': 'test_x2', 'vcpus': 2, 'weight': 30}]}

LICENSE
=======

The MIT License (MIT) 2018, Anton Grudin.

