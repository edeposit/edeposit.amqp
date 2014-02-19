#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import sys
import time
from string import Template


import pika
import daemon  # python-daemon package from pypi
from daemon import runner


#= Variables ==================================================================
SERVER_TEMPLATE = "amqp://$USERNAME:$PASSWORD@$SERVER:$PORT/%2f"  # %2f = /


#= Functions & objects ========================================================


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

        if self.isRunning() and "stop" not in sys.argv:
            print 'It looks like a daemon is already running!'
            exit()

    def start(self):
        try:
            daemon_runner = runner.DaemonRunner(self)
            daemon_runner.do_action()
        except daemon.runner.DaemonRunnerStopFailureError:
            print "There is nothing to kill."
            sys.exit(0)
        except SystemExit:
            self.at_exit()

    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            time.sleep(10)

        self.at_exit()  # this is run only if daemon was not started properly

    def at_exit(self):
        print "exiting"

    def isRunning(self):
        lockfile = runner.make_pidlockfile(self.pidfile_path, 1)

        return lockfile.is_locked()


#= Main program ===============================================================
if __name__ == '__main__':
    a = App()
    a.start()

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
