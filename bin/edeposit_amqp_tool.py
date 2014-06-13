#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pika

# if the module wasn't yet installed at this system, load it from package
try:
    from edeposit.amqp.settings import *
except ImportError:
    sys.path.insert(0, os.path.abspath('../edeposit/'))
    import amqp
    sys.modules["edeposit.amqp"] = amqp


from edeposit.amqp import settings
from edeposit.amqp import amqpdaemon


# Variables ===================================================================



# Functions & objects =========================================================
def create_blocking_connection(host):
    """
    Return properly created blocking connection.

    Args:
        host (str): Host as it is defined in :func:`.get_amqp_settings`.

    Uses :func:`edeposit.amqp.amqpdaemon.getConParams`.
    """
    return pika.BlockingConnection(
        amqpdaemon.getConParams(
            settings.get_amqp_settings()[host.lower()]["vhost"]
        )
    )


def receive(channel, queue):
    """
    Print all messages in queue.
    """
    for method_frame, properties, body in channel.consume(queue):
        print "Message:"
        print method_frame
        print properties
        print body
        print "---"
        print

        channel.basic_ack(method_frame.delivery_tag)


# Main program ================================================================
if __name__ == '__main__':
    pass
