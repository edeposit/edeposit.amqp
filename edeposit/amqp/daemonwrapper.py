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
            self.atIsRunning()

    def run_daemon(self):
        try:
            self.daemon_runner.do_action()
        except daemon.runner.DaemonRunnerStopFailureError:
            self.atStopFail()
        except SystemExit:
            self.atExit()

    def body(self):
        pass

    def run(self):
        try:
            self.body()
        except:
            raise
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
        print "Exiting"

    def isRunning(self):
        return runner.make_pidlockfile(self.pidfile_path, 1).is_locked()
