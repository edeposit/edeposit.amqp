#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Standalone daemon allowing AMQP communication user-management part of the
`FTP module <https://github.com/edeposit/edeposit.amqp.ftp>`_.

::

    ./edeposit_amqp_ftpdaemon.py start/stop/restart [--foreground]

If ``--foreground`` parameter is used, script will not run as daemon, but as
normal script at foreground. Without that, only one (true unix) daemon instance
will be running at the time.
"""
# Imports =====================================================================
import os
import os.path
import sys


from pika.exceptions import ConnectionClosed

from edeposit.amqp.ftp import *
from edeposit.amqp.ftp.structures import *  # for serializers


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
            settings.RABBITMQ_FTP_VIRTUALHOST
        ),
        queue=settings.RABBITMQ_FTP_INPUT_QUEUE,
        out_exch=settings.RABBITMQ_FTP_EXCHANGE,
        out_key=settings.RABBITMQ_FTP_OUTPUT_KEY,
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
