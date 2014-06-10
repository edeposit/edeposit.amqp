#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
"""
Standalone daemon providing AMQP communication with
`Calibre module <http://edeposit-amqp-calibre.readthedocs.org>`_.

This script can be used as aplication, not just as module::

    ./calibredaemon.py start/stop/restart [--foreground]

If ``--foreground`` parameter is used, script will not run as daemon, but as
normal script at foreground. Without that, only one (true unix) daemon instance
will be running at the time.
"""
import os
import os.path
import sys


from edeposit.amqp.calibre import *


# if the module wasn't yet installed at this system, load it from package
try:
    from edeposit.amqp import settings
except ImportError:
    sys.path.insert(0, os.path.abspath('../edeposit/'))
    import amqp
    sys.modules["edeposit.amqp"] = amqp


from edeposit.amqp.amqpdaemon import AMQPDaemon, getConParams
from edeposit.amqp import settings


#= Functions & objects ========================================================
def main():
    """
    Arguments parsing, etc..
    """
    daemon = AMQPDaemon(
        con_param=getConParams(
            settings.RABBITMQ_CALIBRE_VIRTUALHOST
        ),
        queue=settings.RABBITMQ_CALIBRE_DAEMON_QUEUE,
        out_exch=settings.RABBITMQ_CALIBRE_EXCHANGE,
        out_key=settings.RABBITMQ_CALIBRE_PLONE_KEY,
        react_fn=reactToAMQPMessage,
        glob=globals()              # used in deserializer
    )

    if "--foreground" in sys.argv:  # run at foreground
        daemon.run()
    else:
        daemon.run_daemon()         # run as daemon


#= Main program ===============================================================
if __name__ == '__main__':
    main()
