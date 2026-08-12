Contributing
============

Use Python 3.11 or newer and install development tools with
``python -m pip install -e '.[dev]'``. Then run:

.. code-block:: console

   python -m ruff check .
   python -m ruff format --check .
   python -m unittest discover -v
   python -m build
   python -m twine check dist/*

Normal tests are offline and must not need a CloudVPS token. Add every new
provider operation to ``cloudvps/endpoints.json``, its resource wrapper, request
contract tests, and ``docs/API.rst``. Significant behavior changes begin as an
OpenSpec change under ``openspec/changes``.

Live tests are opt-in. Supply ``CLOUDVPS_TOKEN`` only through the environment;
never commit it or paste it into failure output. Run read-only checks with
``python -m unittest tests.test_live.ReadOnlyLiveTests -v``. The mutating suite
also requires ``CLOUDVPS_FULL_INTEGRATION=1`` and
``CLOUDVPS_TEST_PUBLIC_KEY``. It creates billable temporary resources, so use a
dedicated account where possible, review the selected region/plan/image, and
inspect the printed cleanup report before considering the run complete.
