#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
"""
Generic AMQP blockin communication daemon.

Usage is simple - just inherit the class and override onMessageReceived().

You can send messages back with 
"""
import pika


import settings
import daemonwrapper


#= Functions & objects ========================================================
class PikaDaemon(daemonwrapper.DaemonRunnerWrapper):
    """
    Pika daemon handling connections.
    """
    def __init__(self, virtual_host, queue, output_exchange, routing_key,
                 output_key=None):
        """
        virtual_host -- rabbitmq's virtualhost
        queue -- name of queue where the daemon should listen
        output_exchange -- name of exchange where the daemon shoud put
                           responses,
        routing_key -- input routing key
        output_key -- Output exchange routing key. If not set, routing_key is
                      used.
        """
        super(PikaDaemon, self).__init__(queue)
        self.queue = queue
        self.output_exchange = output_exchange
        self.routing_key = routing_key
        self.virtual_host = virtual_host

        self.content_type = "application/json"

        self.output_key = output_key
        if output_key is None:
            self.output_key = self.routing_key

    def body(self):
        """
        This method just handles AMQP connection details and receive loop.
        """
        self.connection = pika.BlockingConnection(  # set connection details
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=int(settings.RABBITMQ_PORT),
                virtual_host=self.virtual_host,
                credentials=pika.PlainCredentials(
                    settings.RABBITMQ_USER_NAME,
                    settings.RABBITMQ_USER_PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()

        # receive messages and put them to .onMessageReceived() callback
        for method_frame, properties, body in self.channel.consume(self.queue):
            self.onMessageReceived(method_frame, properties, body)
            self.channel.basic_ack(method_frame.delivery_tag)

    def onMessageReceived(self, method_frame, properties, body):
        """
        Callback which is called everytime when message is received.

        You should probably redefine this.
        """
        print "method_frame:", method_frame
        print "properties:", properties
        print "body:", body

        print "---"
        print

    def sendMessage(self, exchange, routing_key, message, properties=None):
        """
        With this function, you can send message to `exchange`.

        exchange -- name of exchange you want to message to be delivered
        routing_key -- which routing key to use in headers of message
        message -- body of message
        properties -- properties of message - if not used, or set to None, 
                      self.content_type and delivery_mode=1 is used
        """
        if properties is None:
            properties = pika.BasicProperties(
                content_type=self.content_type,
                delivery_mode=1
            )

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            body=message
        )

    def sendResponse(self, message):
        """
        Send `message` to self.output_exchange with routing key self.output_key
        and self.content_type in delivery_mode=1.
        """
        self.sendMessage(
            self.output_exchange,
            self.output_key,
            message
        )

    def onExit(self):
        """
        Called when daemon is stopped. Basically just AMQP .close() functions
        to ensure clean exit.

        You can override this, but don't forget to call it thru super(), or
        AMQP communication wouldn't be closed properly!
        """
        try:
            if hasattr(self, "channel"):
                self.channel.cancel()
                self.channel.close()
                self.connection.close()
        except pika.exceptions.ChannelClosed:
            pass
