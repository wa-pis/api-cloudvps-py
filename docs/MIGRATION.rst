Migrating from 0.1.7 to 0.2.0
==============================

* Python 2 and Python 3.4-3.10 are no longer supported. Use Python 3.11-3.14.
* ``from cloudvps import Api`` and historical v1 resource aliases still work.
* Prefer ``base_url="https://host"`` over the deprecated ``provider="host"``.
* Use explicit ``api.v1`` and ``api.v2`` namespaces in new code.
* HTTP failures now raise ``CloudVpsAPIError`` instead of returning the provider
  error JSON as though it were successful data.
* Successful ``204`` and empty responses return ``None``; legacy DELETE status
  integers are no longer returned.
* Every request now has a 30-second default timeout.
* PTR updates moved from ``api.vps.ptr(server_id, ptr)`` to
  ``api.v1.ips.update_ptr(ip_address, ptr)``.
* ``rebuild(..., ssh_keys=None)`` no longer sends ``[None]``.

The following old calls target endpoints absent from the current provider
OpenAPI contract. During 0.2.x they remain importable, emit
``DeprecationWarning``, and fail before networking: ``common.estimate``,
``common.validate``, ``actions.list``, ``history.get``, image get/rename/delete,
snapshot get/rename, ``vps.get_vnc``, and server-based ``vps.ptr``. Deprecated
entry points may be removed in 1.0.0.
