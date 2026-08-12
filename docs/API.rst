API reference
=============

All methods return the provider's decoded dictionaries/lists without model
conversion. Successful empty responses return ``None``. Non-success responses
raise ``CloudVpsAPIError``.

Client
------

``Api(token, *, base_url="https://api.cloudvps.reg.ru", timeout=30, session=None)``
creates a synchronous client. A caller-supplied Requests session remains owned
by the caller. Internally created sessions can be closed with ``close()`` or a
context manager. No request is retried automatically.

API v1
------

===============================  ======  =================================================
Client method                    HTTP    Provider path
===============================  ======  =================================================
``feedback.account(email, msg)`` POST    ``/v1/account/feedback``
``feedback.hook(email, msg)``    POST    ``/v1/feedback``
``ssh_keys.list()``              GET     ``/v1/account/keys``
``ssh_keys.create(name, key)``   POST    ``/v1/account/keys``
``ssh_keys.rename(id, name)``    PUT     ``/v1/account/keys/{key_id}``
``ssh_keys.delete(id)``          DELETE  ``/v1/account/keys/{key_id}``
``settings.get(key)``            GET     ``/v1/account/settings/{key}``
``settings.update(key, value)``  PUT     ``/v1/account/settings/{key}``
``actions.get(id)``              GET     ``/v1/actions/{action_id}``
``billing.balance()``            GET     ``/v1/balance_data``
``billing.history()``            GET     ``/v1/billing_history``
``billing.prices()``             GET     ``/v1/prices``
``history.list(limit, offset)``  GET     ``/v1/history``
``images.list(...)``             GET     ``/v1/images``
``ips.list(reglet_id=...)``      GET     ``/v1/ips``
``ips.create(...)``              POST    ``/v1/ips``
``ips.update_ptr(ip, ptr)``      PUT     ``/v1/ips/{ip}``
``ips.delete(ip)``               DELETE  ``/v1/ips/{ip}``
``kubernetes.get_kubeconfig(id)`` GET    ``/v1/k8s_clusters/{id}/get_kubeconfig``
``common.get_new_name()``        GET     ``/v1/random_reglet_name``
``common.sizes()``               GET     ``/v1/sizes``
``common.reglets_for_snapshot()`` GET    ``/v1/reglets_for_snapshot/{id}``
``servers.list()``               GET     ``/v1/reglets``
``servers.create(...)``          POST    ``/v1/reglets``
``servers.get(id)``              GET     ``/v1/reglets/{id}``
``servers.rename(id, name)``     PUT     ``/v1/reglets/{id}``
``servers.delete(id)``           DELETE  ``/v1/reglets/{id}``
``servers.action(id, type, ...)`` POST   ``/v1/reglets/{id}/actions``
``removed_servers.list()``       GET     ``/v1/removed_servers``
``snapshots.list(region=...)``   GET     ``/v1/snapshots``
``snapshots.delete(id)``         DELETE  ``/v1/snapshots/{image_id}``
``vpcs.list()``                  GET     ``/v1/vpcs``
``vpcs.create(name)``            POST    ``/v1/vpcs``
``vpcs.get(id)``                 GET     ``/v1/vpcs/{id}``
``vpcs.rename(id, name)``        PUT     ``/v1/vpcs/{id}``
``vpcs.delete(id)``              DELETE  ``/v1/vpcs/{id}``
``vpcs.members(id)``             GET     ``/v1/vpcs/{id}/members``
``vpcs.attach(id, resource_id)`` POST    ``/v1/vpcs/{id}/members``
``vpcs.detach(id, resource_id)`` DELETE  ``/v1/vpcs/{id}/members/{resource_id}``
===============================  ======  =================================================

Parameters and return values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Path identifiers are passed as the positional ``id``, ``ip``, or
``resource_id`` shown in the table. Feedback methods take ``user_email`` and
``message``; key methods take ``name`` and ``public_key``; settings updates take
``value``. ``history.list`` accepts ``limit`` and ``offset``.

``images.list`` accepts ``type``, ``private``, ``reglet_id``, ``group``, and
``region``. ``ips.list`` filters by ``reglet_id``; ``ips.create`` takes
``reglet_id``, ``ipv4_count``, and ``ipv6_count``. PTR updates take a concrete
IPv4 or IPv6 address and ``ptr``. Snapshot listing accepts ``region``.

``servers.create(name=None, size=..., image=..., ssh_keys=None, *,
backups=None, floating_ip=None, isp_license_size=None, promocode=None,
region_slug=None)`` requires ``size`` and ``image`` and omits every unset field.
VPC create/rename take ``name`` and attach/detach take the server
``resource_id``.

Responses are returned exactly as decoded from the provider schema: envelopes,
lists, pagination metadata, and action objects are not renamed or converted.
Successful 204 or empty responses return ``None``. All HTTP error responses use
``CloudVpsAPIError``; transport errors remain Requests exceptions.

Server action helpers
~~~~~~~~~~~~~~~~~~~~~

Convenience methods exist for ``start``, ``stop``, ``reboot``, ``rebuild``,
``password_reset``, ``resize``, ``generate_vnc_link`` (also ``request_vnc``),
``snapshot``, ``enable_backups``, ``disable_backups``, ``restore``, ``clone``,
and ``resize_isp_license``. They all use the documented server action endpoint.

API v2
------

``api.v2.images.list(region, page=1, items_per_page=100, *, private=None,
type=None)`` maps to ``GET /v2/images``.

``api.v2.plans.list(region, page=1, items_per_page=100, *, vcpus=None,
disk=None, memory=None, plan_line=None, unit=None)`` maps to
``GET /v2/plans``.

Both return one provider page with its ``metadata``. They never fetch subsequent
pages implicitly and pass future non-empty region slugs through to the provider.
``page``, ``items_per_page``, and ``region`` are sent on every request.
``images.list`` additionally accepts ``private`` and ``type``. ``plans.list``
additionally accepts ``vcpus``, ``disk``, ``memory``, ``plan_line``, and
``unit``; unset optional filters are omitted.
