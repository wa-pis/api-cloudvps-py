.. image:: https://badge.fury.io/py/api-cloudvps-py.svg
   :target: https://badge.fury.io/py/api-cloudvps-py
.. image:: https://badge.fury.io/gh/wa-pis%2Fapi-cloudvps-py.svg
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
`order free service <https://www.reg.ru/vps/cloud>`__

More info about reg.ru kvm cloud https://www.reg.ru/vps/cloud

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
    {'sizes': [{'disk': 10, 'id': 5, 'memory': 512, 'name': 'Cloud-1', 'price': '0.30', 'price_month': 199, 'slug': 'cloud-1', 'vcpus': 1, 'weight': 10}, {'disk': 20, 'id': 1, 'memory': 1024, 'name': 'Cloud-2', 'price': '0.67', 'price_month': 449, 'slug': 'cloud-2', 'vcpus': 2, 'weight': 20}, {'disk': 40, 'id': 3, 'memory': 2048, 'name': 'Cloud-3', 'price': '1.34', 'price_month': 899, 'slug': 'cloud-3', 'vcpus': 2, 'weight': 30}, {'disk': 60, 'id': 7, 'memory': 4096, 'name': 'Cloud-4', 'price': '2.66', 'price_month': 1790, 'slug': 'cloud-4', 'vcpus': 2, 'weight': 40}, {'disk': 60, 'id': 9, 'memory': 6144, 'name': 'Cloud-5', 'price': '3.71', 'price_month': 2490, 'slug': 'cloud-5', 'vcpus': 2, 'weight': 50}, {'disk': 80, 'id': 11, 'memory': 8192, 'name': 'Cloud-6', 'price': '4.75', 'price_month': 3190, 'slug': 'cloud-6', 'vcpus': 4, 'weight': 60}]}

LICENSE
=======

The MIT License (MIT) 2018, Anton Grudin.

