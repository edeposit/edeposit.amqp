#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
AMQP tool used for debugging and automatic RabbitMQ schema making.
"""
# Imports =====================================================================
import os
import sys
import uuid
import os.path
import argparse


import pika

# if the module wasn't yet installed at this system, load it from package
try:
    import edeposit.amqp.settings as settings
    import edeposit.amqp.amqpdaemon as amqpdaemon
except ImportError:
    sys.path.insert(0, os.path.abspath('../edeposit/amqp'))

    import settings
    import amqpdaemon


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
    """
    Create exchanges, queues and route them.

    Args:
        host (str): One of the possible hosts.
    """
    connection = create_blocking_connection(host)
    channel = connection.channel()

    exchange = settings.get_amqp_settings()[host]["exchange"]
    channel.exchange_declare(
        exchange=exchange,
        exchange_type="topic",
        durable=True
    )
    print "Created exchange '%s'." % exchange
    print "Creating queues:"

    queues = settings.get_amqp_settings()[host]["queues"]
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


def send_message(host, data, timeout=None):
    connection = create_blocking_connection(host)

    # register timeout
    if timeout >= 0:
        connection.add_timeout(
            timeout,
            lambda: sys.stderr.write("Timeouted!\n") or sys.exit(1)
        )

    channel = connection.channel()

    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=1,
        headers={"UUID": str(uuid.uuid4())}
    )

    parameters = settings.get_amqp_settings()[host]

    channel.basic_publish(
        exchange=parameters["exchange"],
        routing_key=parameters["in_key"],
        properties=properties,
        body=data
    )


def get_hosts():
    """
    Returns:
        list: List of strings with names of possible hosts.
    """
    return settings.get_amqp_settings().keys()


def require_host_parameter(args):
    if not args.host:
        sys.stderr.write("--host is required parameter to --create!\n")
        sys.exit(1)


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
    parser.add_argument(
        "-g",
        "--host",
        choices=get_hosts() + ["all"],
        help="""Specify host. You can get list of valid host by using --list
                switch or use 'all' for all hosts."""
    )
    parser.add_argument(
        "-c",
        "--create",
        action='store_true',
        help="""Create exchanges/queues/routes for given host. --host is
                required."""
    )
    parser.add_argument(
        "-p",
        "--put",
        help="""Put message into input queue at given host. --put argument
                expects file with JSON data or - as indication of stdin data
                input."""
    )
    parser.add_argument(
        '--timeout',
        metavar="N",
        type=int,
        default=-1,
        help="Wait for message only N seconds."
    )
    args = parser.parse_args()

    if args.list:
        print "\n".join(get_hosts())
        sys.exit(0)

    if args.create:
        require_host_parameter(args)

        if args.host == "all":
            for host in get_hosts():
                create_schema(host)
        else:
            create_schema(args.host)

    elif args.put:
        require_host_parameter(args)

        data = None
        if args.put == "-":
            data = sys.stdin.read()
        else:
            if not os.path.exists(args.put):
                sys.stderr.write("Can't open '%s'!\n" % args.put)
                sys.exit(1)

            with open(args.put) as f:
                data = f.read()

        send_message(host, data, args.timeout)
