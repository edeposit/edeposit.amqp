#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import sys
import os.path
import argparse


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


def create_schema(host):
    connection = create_blocking_connection(host)
    channel = connection.channel()

    exchange = settings.get_amqp_settings()[vhost]["exchange"]
    channel.exchange_declare(
        exchange=exchange,
        exchange_type="topic",
        durable=True
    )
    print "Created exchange '%s'." % exchange

    print "Creating queues:"
    queues = settings.get_amqp_settings()[vhost]["queues"]
    for queue in queues.keys():
        channel.queue_declare(
            queue=queue,
            durable=True,
            # arguments={'x-message-ttl': int(1000 * 60 * 60 * 24)} # :S
        )
        print "\tCreated durable queue '%s'." % queue

    print
    print "Routing exchanges using routing key to queues:"

    for queue in queues.keys():
        channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=queues[queue]
        )

        print "\tRouting exchange %s['%s'] -> '%s'." % (
            exchange,
            queues[queue],
            queue
        )

# Main program ================================================================
if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(
        description="""AMQP tool used for debugging and automatic RabbitMQ
                       schema making."""
    )
    parser.add_argument(
        "-l",
        "--list",
        action='store_true',
        help="List all possible hosts."
    )
    args = parser.parse_args()
