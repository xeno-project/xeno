Xeno Connector
==========================

The Xeno Connector connects the ViUR framework with various open source alternatives to the google cloud.

It uses:
 - `gunicorn`_ as web server
 - `apscheduler`_ for deferred tasks and cron
 - `mongodb`_ as database

more databases are planned:
 - unqlite
 - arangodb

WARNING - WIP
--------------------

Currently this connector is WIP and unstable. Do not use this connector in a production system.

License
-------

GNU Lesser General Public License v3.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/xeno-project/xeno/blob/master/LICENSE
.. _unqlite: https://github.com/coleifer/unqlite-python
.. _gunicorn: https://github.com/benoitc/gunicorn
.. _apscheduler: https://github.com/agronholm/apscheduler
.. _mongodb: https://github.com/mongodb/mongo-python-driver
