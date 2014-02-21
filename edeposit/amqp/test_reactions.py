#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import aleph
import aleph.convertors

import settings

import pika


#= Main program ===============================================================
if __name__ == '__main__':
    isbnq = aleph.ISBNQuery("80-251-0225-4")
    request = aleph.SearchRequest(isbnq, "trololo")
    json_data = aleph.convertors.toJSON(request)

    connection = pika.BlockingConnection(  # set connection details
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
    channel = connection.channel()

    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=1
    )

    channel.basic_publish(
        exchange=settings.RABBITMQ_ALEPH_EXCHANGE,
        routing_key=settings.RABBITMQ_ALEPH_DAEMON_KEY,
        properties=properties,
        body=json_data
    )

    for method_frame, properties, body in channel.consume(settings.RABBITMQ_ALEPH_PLONE_QUEUE):
        print "Message:"
        print method_frame
        print properties
        print body
        print "---"
        print

        channel.basic_ack(method_frame.delivery_tag)
