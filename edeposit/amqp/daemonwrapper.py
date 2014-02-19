#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import sys


import daemon  # python-daemon package from pypi
from daemon import runner


class DaemonRunnerWrapper(object):
    def __init__(self, name):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/' + name + '.pid'
        self.pidfile_timeout = 5

        self.daemon_runner = runner.DaemonRunner(self)
        if self.isRunning():
            self.onIsRunning()

    def run_daemon(self):
        try:
            self.daemon_runner.do_action()
        except daemon.runner.DaemonRunnerStopFailureError:
            self.onStopFail()
        except SystemExit:
            self.onExit()

    def body(self):
        pass

    def run(self):
        try:
            self.body()
        except:
            raise
        finally:           # this is called only if daemon was not started
            self.onExit()  # and whole app runned on foreground

    def onStopFail(self):
        print "There is no running instance to be stopped."
        sys.exit(0)

    def onIsRunning(self):
        if "stop" not in sys.argv and "restart" not in sys.argv:
            print 'It looks like a daemon is already running!'
            sys.exit(1)

    def onExit(self):
        print "DaemonRunnerWrapper shutdown."

    def isRunning(self):
        return runner.make_pidlockfile(self.pidfile_path, 1).is_locked()
