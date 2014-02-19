#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
from string import Template


import pika


import daemonwrapper


#= Variables ==================================================================
SERVER_TEMPLATE = "amqp://$USERNAME:$PASSWORD@$SERVER:$PORT/%2f"  # %2f = /


#= Functions & objects ========================================================
class PikaDaemon(daemonwrapper.DaemonRunnerWrapper):
    def __init__(self, name):
        super(PikaDaemon, self).__init__(name)
        self.name = name
        # DaemonRunnerWrapper.__init__(self, name)

    def body(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()

        for method_frame, properties, body in self.channel.consume(self.name):
            print body

    def atExit(self):
        try:
            self.channel.cancel()
            self.channel.close()
            self.connection.close()
        except pika.exceptions.ChannelClosed:
            pass



#= Main program ===============================================================
if __name__ == '__main__':
    a = PikaDaemon("daemon")
    a.run_daemon()
    # a.run()

    # connection = pika.BlockingConnection(
    #     pika.URLParameters(
    #         Template(SERVER_TEMPLATE).substitute(
    #             USERNAME=settings.RABBITMQ_USER_NAME,
    #             PASSWORD=settings.RABBITMQ_USER_PASSWORD,
    #             SERVER=settings.RABBITMQ_HOST,
    #             PORT=settings.RABBITMQ_PORT
    #         )
    #     )
    # )
