#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Standalone daemon providing AMQP communication with
`Aleph module <https://github.com/jstavel/edeposit.amqp.aleph>`_.

::

    ./alephdaemon.py start/stop/restart [--foreground]

If ``--foreground`` parameter is used, script will not run as daemon, but as
normal script at foreground. Without that, only one (true unix) daemon instance
will be running at the time.
"""
# Imports =====================================================================
import os
import os.path
import sys


from pika.exceptions import ConnectionClosed

from edeposit.amqp.aleph import *
from edeposit.amqp.aleph.datastructures import *  # for serializers


# if the module wasn't yet installed at this system, load it from package
try:
    from edeposit.amqp import settings
except ImportError:
    sys.path.insert(0, os.path.abspath('../edeposit/'))
    import amqp
    sys.modules["edeposit.amqp"] = amqp

from edeposit.amqp import settings
from edeposit.amqp.amqpdaemon import AMQPDaemon, getConParams


# Functions & objects =========================================================
def main():
    """
    Arguments parsing, etc..
    """
    daemon = AMQPDaemon(
        con_param=getConParams(
            settings.RABBITMQ_ALEPH_VIRTUALHOST
        ),
        queue=settings.RABBITMQ_ALEPH_INPUT_QUEUE,
        out_exch=settings.RABBITMQ_ALEPH_EXCHANGE,
        out_key=settings.RABBITMQ_ALEPH_OUTPUT_KEY,
        react_fn=reactToAMQPMessage,
        glob=globals()                # used in deserializer
    )

    if "--foreground" in sys.argv:  # run at foreground
        daemon.run()
    else:
        daemon.run_daemon()         # run as daemon


# Main program ================================================================
if __name__ == '__main__':
    try:
        main()
    except ConnectionClosed as e:
        sys.stderr.write(
            e.message + " - is the RabbitMQ queues properly set?\n"
        )
        sys.exit(1)
