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
class DaemonRunnerWrapper():
    def __init__(self, name):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/' + name + '.pid'
        self.pidfile_timeout = 5

        self.daemon_runner = runner.DaemonRunner(self)
        if self.isRunning():
            self.atIsRunning()

    def start_daemon(self):
        try:
            self.daemon_runner.do_action()
        except daemon.runner.DaemonRunnerStopFailureError:
            self.atStopFail()
        except SystemExit:
            self.atExit()

    def body(self):
        # self.connection = pika.BlockingConnection()
        # self.channel = connection.channel()
        while True:
            print "xe"
            time.sleep(5)

    def run(self):
        try:
            self.body()
        except:
            pass
        finally:            # this is called only if daemon was not started
            self.atExit()  # and whole app runned on foreground

    def atStopFail(self):
        print "There is no running instance to be stopped."
        sys.exit(0)

    def atIsRunning(self):
        if "stop" not in sys.argv:
            print 'It looks like a daemon is already running!'
            sys.exit(1)

    def atExit(self):
        print "exiting"

    def isRunning(self):
        lockfile = runner.make_pidlockfile(self.pidfile_path, 1)

        return lockfile.is_locked()


#= Main program ===============================================================
if __name__ == '__main__':
    a = DaemonRunnerWrapper("daemon")
    a.start_daemon()
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
