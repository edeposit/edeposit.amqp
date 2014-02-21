#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import sys


import aleph
import aleph.convertors

import settings

import pika


def createBlockingConnection():
    return pika.BlockingConnection(  # set connection details
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_ALEPH_VIRTUALHOST,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USER_NAME,
                settings.RABBITMQ_USER_PASSWORD
            )
        )
    )


def receive():
    for method_frame, properties, body in channel.consume(settings.RABBITMQ_ALEPH_PLONE_QUEUE):
        print "Message:"
        print method_frame
        print properties
        print body
        print "---"
        print

        channel.basic_ack(method_frame.delivery_tag)


def createSchema():
    exchanges = [
        "search",
        "count",
        "export"
    ]
    queues = {
        "plone": "result",
        "daemon": "request"
    }

    connection = createBlockingConnection()
    channel = connection.channel()

    for exchange in exchanges:
        channel.exchange_declare(
            exchange=exchange,
            exchange_type="topic",
            durable=True
        )

    for queue in queues.keys():
        channel.queue_declare(
            queue=queue,
            durable=True,
            # arguments={'x-message-ttl': int(1000 * 60 * 60 * 24)} # :S
        )

    for exchange in exchanges:
        for queue in queues.keys():
            channel.queue_bind(
                queue=queue,
                exchange=exchange,
                routing_key=queues[queue]
            )


#= Main program ===============================================================
if __name__ == '__main__':
    isbnq = aleph.ISBNQuery("80-251-0225-4")
    request = aleph.SearchRequest(isbnq, "trololo")
    json_data = aleph.convertors.toJSON(request)

    connection = createBlockingConnection()
    channel = connection.channel()

    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=1
    )

    if "--create" in sys.argv:
        createSchema()

    if "--put" in sys.argv:
        channel.basic_publish(
            exchange=settings.RABBITMQ_ALEPH_EXCHANGE,
            routing_key=settings.RABBITMQ_ALEPH_DAEMON_KEY,
            properties=properties,
            body=json_data
        )

    if "--get" in sys.argv:
        try:
            receive()
        except KeyboardInterrupt:
            print
            sys.exit(0)

    if len(sys.argv) == 1:
        print "Usage " + sys.argv[0] + " [--get] [--put]"