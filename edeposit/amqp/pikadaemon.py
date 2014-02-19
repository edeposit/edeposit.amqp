#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import pika


import settings
import daemonwrapper


#= Functions & objects ========================================================
class PikaDaemon(daemonwrapper.DaemonRunnerWrapper):
    def __init__(self, virtual_host, queue, output_exchange, routing_key,
                 output_key=None):
        """
        Pika daemon handling connections.

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

        self.output_key = output_key
        if output_key is None:
            self.output_key = self.routing_key

    def body(self):
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

    def sendMessage(self, message):
        """
        Callback which allows you to send message.
        """
        self.channel.basic_publish(
            exchange=self.output_exchange,
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=1
            ),
            body=message
        )

    def onExit(self):
        """
        Called when daemon is stopped. Basically just AMQP .close() functions
        to ensure clean exit.
        """
        try:
            if hasattr(self, "channel"):
                self.channel.cancel()
                self.channel.close()
                self.connection.close()
        except pika.exceptions.ChannelClosed:
            pass


#= Main program ===============================================================
if __name__ == "__main__":
    a = PikaDaemon("daemon")
    a.run_daemon()
    # a.run()
