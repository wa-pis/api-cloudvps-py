api-cloudvps-py
===============

|PyPI| |Python| |CI|

An unofficial synchronous Python client for the `REG.Cloud CloudVPS API`_.
It covers every operation currently published in the CloudVPS `API v1`_ and
`API v2`_ OpenAPI contracts.

This project is maintained independently and is not an official REG.Cloud SDK.

Requirements
------------

Python 3.11 through 3.14 are supported.

Installation
------------

.. code-block:: console

   python -m pip install api-cloudvps-py

Authentication
--------------

Create an API token in the REG.Cloud control panel and keep it outside source
code. For example:

.. code-block:: console

   export CLOUDVPS_TOKEN='replace-with-your-token'

.. code-block:: python

   import os

   from cloudvps import Api

   with Api(os.environ["CLOUDVPS_TOKEN"]) as api:
       sizes = api.v1.common.sizes()
       plans = api.v2.plans.list("openstack-sam1", items_per_page=10)

The default request timeout is 30 seconds. Set a scalar or a Requests-style
connect/read tuple when necessary:

.. code-block:: python

   api = Api(os.environ["CLOUDVPS_TOKEN"], timeout=(5, 60))

Quick examples
--------------

The following operations only read account or catalog state:

.. code-block:: python

   servers = api.v1.servers.list()
   images = api.v2.images.list(
       "openstack-sam1",
       page=1,
       items_per_page=10,
       type="distribution",
   )
   balance = api.v1.billing.balance()

The next example creates a billable server and deletes it. Review the selected
plan, image, region, and resulting charges before executing it:

.. code-block:: python

   created = api.v1.servers.create(
       "api-client-example",
       "c1-m1-d10-hp",
       "ubuntu-24-04-amd64",
       region_slug="openstack-sam1",
       backups=False,
   )
   server_id = created["reglet"]["id"]
   api.v1.servers.delete(server_id)

The following calls also change infrastructure and may affect availability or
cost. Inspect their responses and remove temporary resources promptly:

.. code-block:: python

   ip_result = api.v1.ips.create(server_id, ipv4_count=1)
   snapshot_action = api.v1.servers.snapshot(server_id, "before-upgrade", offline=True)
   network = api.v1.vpcs.create("private-network")
   vpc_id = network["resource_id"]
   attach_action = api.v1.vpcs.attach(vpc_id, server_id)

   # After the provider actions finish:
   api.v1.vpcs.detach(vpc_id, server_id)

   # CloudVPS currently keeps private networks: vpcs.delete() returns HTTP 501.

Errors
------

Non-success HTTP responses raise ``CloudVpsAPIError``. The exception exposes
``status_code``, ``code``, and ``message`` where supplied by the provider. Bearer
tokens are redacted from exception text.

.. code-block:: python

   from cloudvps import CloudVpsAPIError

   try:
       api.v1.servers.get(123)
   except CloudVpsAPIError as error:
       print(error.status_code, error.code, error.message)

API versions and compatibility
------------------------------

Use ``api.v1`` for operational resources and ``api.v2`` for regional plans and
images. The historical ``api.ssh``, ``api.common``, ``api.history``,
``api.snapshots``, ``api.images``, ``api.actions``, and ``api.vps`` accessors
remain aliases for v1 in the 0.2 release line.

See `API reference`_ for all methods and `migration guide`_ before upgrading
from 0.1.7.

Terraform or Python?
--------------------

Use the official `REG.Cloud Terraform provider`_ for declarative lifecycle
management of servers, GPU servers, SSH keys, and snapshots. Use this Python
client for imperative automation and for the wider CloudVPS surface such as
billing, IP addresses, private networks, actions, and account history. This
package does not replace Terraform.

Development and releases
------------------------

See `contributing guide`_, `security policy`_, and `release runbook`_. Releases
are published from GitHub Actions through PyPI Trusted Publishing; no long-lived
PyPI upload token is stored in the repository.

License
-------

MIT, copyright Anton Grudin.

.. |PyPI| image:: https://img.shields.io/pypi/v/api-cloudvps-py.svg
   :target: https://pypi.org/project/api-cloudvps-py/
.. |Python| image:: https://img.shields.io/pypi/pyversions/api-cloudvps-py.svg
   :target: https://pypi.org/project/api-cloudvps-py/
.. |CI| image:: https://github.com/wa-pis/api-cloudvps-py/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/wa-pis/api-cloudvps-py/actions/workflows/ci.yml
.. _REG.Cloud CloudVPS API: https://developers.cloudvps.reg.ru/
.. _API v1: https://api.cloudvps.reg.ru/v1/ui/
.. _API v2: https://api.cloudvps.reg.ru/v2/
.. _REG.Cloud Terraform provider: https://reg.cloud/support/cloud/instrumenty/terraform
.. _API reference: https://github.com/wa-pis/api-cloudvps-py/blob/master/docs/API.rst
.. _migration guide: https://github.com/wa-pis/api-cloudvps-py/blob/master/docs/MIGRATION.rst
.. _contributing guide: https://github.com/wa-pis/api-cloudvps-py/blob/master/CONTRIBUTING.rst
.. _security policy: https://github.com/wa-pis/api-cloudvps-py/blob/master/SECURITY.md
.. _release runbook: https://github.com/wa-pis/api-cloudvps-py/blob/master/docs/RELEASING.md
