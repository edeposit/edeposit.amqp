edeposit_amqp_alephdaemon.py script
===================================

.. automodule:: edeposit_amqp_alephdaemon

Help
----
::

    $ ./edeposit_amqp_alephdaemon.py -husage: edeposit_amqp_alephdaemon.py start/stop/restart [-f] FN

    Aleph communicator. This daemon provides AMQP API for aleph module.

    positional arguments:
      start/stop/restart  Start/stop/restart the daemon.

    optional arguments:
      -h, --help          show this help message and exit
      -f, --foreground    Run at foreground, not as daemon. If not set, script is
                          will run at background as unix daemon.


Example usage::

    ./edeposit_amqp_alephdaemon.py start
    started with pid 4595

or::

    $ ./edeposit_amqp_alephdaemon.py start --foreground

In this case, the script runs as normal program, and it is not daemonized.

Stopping::

    $ ./edeposit_amqp_alephdaemon.py stop
    No handlers could be found for logger "pika.adapters.base_connection"

Don't be concerned by warnings when stopping the daemon, it is just something
that out communication library does.