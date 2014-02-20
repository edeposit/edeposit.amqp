#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 Unported License
# (http://creativecommons.org/licenses/by/3.0/).
#
#= Imports ====================================================================
import sys


import pikadaemon
from aleph import reactToAMQPMessage


#= Functions & objects ========================================================
class AlephDaemon(pikadaemon.PikaDaemon):
    def onMessageReceived(self, method_frame, properties, body):
        try:
            reactToAMQPMessage(body, self.sendResponse)
            return True
        except ValueError, e:
            print e
            return False  # TODO: add reactions to exceptions into protocol

    def sendResponse(self, message):
        print message


#= Main program ===============================================================
if __name__ == '__main__':
    daemon = AlephDaemon(
        virtual_host="aleph",
        queue="aleph-search",
        output_exchange="aleph-search",
        routing_key="search.request",
        output_key="search.reponse"
    )

    if "--foreground" in sys.argv:  # run at foreground
        daemon.run()
    else:
        daemon.run_daemon()  # run as daemon
