Introduction
============

This module contains common parts shared with other AMQP modules from
`Edeposit <http://edeposit.nkp.cz/>`_ project. Main purpose is to provide
configuration data to AMQP server and generic daemons, to run the modules.

Installation
------------
Module is hosted at `PYPI <https://pypi.python.org/pypi/edeposit.amqp>`_, 
and can be easily installed using `PIP
<http://en.wikipedia.org/wiki/Pip_%28package_manager%29>`_:

::

    pip install edeposit.amqp

Source code can be found at `GitHub <https://github.com/>`_: https://github.com/edeposit/edeposit.amqp

Documentation
-------------
Full module documentation is hosted at ReadTheDocs: http://edeposit-amqp.readthedocs.org

Content
=======
Content can be divided between generic modules to support AMQP communication and scripts, which provides ability to test and tweak AMQP communication.

Scripts
-------
Scripts should be automatically installed to your ``$PATH``.

edeposit_amqp_alephdaemon.py
++++++++++++++++++++++++++++

Daemon providing AMQP communication with the `edeposit.amqp.aleph <https://github.com/edeposit/edeposit.amqp.aleph>`_ module.

edeposit_amqp_calibre.py
++++++++++++++++++++++++
Daemon providing AMQP communication with the `edeposit.amqp.calibre  <https://github.com/edeposit/edeposit.amqp.calibre>`_ module.

edeposit_amqp_amqp_tool.py
++++++++++++++++++++++++++

Script for testing the communication and creating
exchanges/queues/routes in `RabbitMQ <https://www.rabbitmq.com/>`_.

Modules
-------

edeposit.amqp.settings
++++++++++++++++++++++

Configuration for RabbitMQ server and E-deposit client modules connecting
into it.

edeposit.amqp.daemonwrapper
+++++++++++++++++++++++++++

Class for spawning Unix daemons.

edeposit.amqp.pikadaemon
++++++++++++++++++++++++

Generic AMQP blocking communication daemon server.

Unittests
================
`pytest <http://pytest.org/>`__ is used to test the code.
You can find the tests in ``edeposit/amqp/tests`` directory.

Tests can be invoked by running ``./run_tests.sh`` script::

    $ ./run_tests.sh -a
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2
    collected 8 items 

    edeposit/amqp/tests/test_daemon.txt .
    edeposit/amqp/tests/integration/test_aleph.py started with pid 18108
    sending response result
    ..No handlers could be found for logger "pika.adapters.base_connection"

    edeposit/amqp/tests/integration/test_daemons.py .
    edeposit/amqp/tests/integration/test_package.py ..
    edeposit/amqp/tests/unittests/test_settings.py ..

    ========================== 8 passed in 14.43 seconds ===========================
