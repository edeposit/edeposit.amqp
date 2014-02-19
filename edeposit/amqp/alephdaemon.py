#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 Unported License
# (http://creativecommons.org/licenses/by/3.0/).
#
#= Imports ====================================================================
import pikadaemon


#= Variables ==================================================================



#= Functions & objects ========================================================
class AlephDaemon(pikadaemon.PikaDaemon):
    def onMessageReceived(self, method_frame, properties, body):
        print "AlephDaemon"
        print body

#= Main program ===============================================================
if __name__ == '__main__':
    a = AlephDaemon("/", "daemon", "daemon", "test", "test")
    a.run_daemon()
    # a.run()
