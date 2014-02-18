#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import time
from daemon import runner  # python-daemon package from pypi


#= Variables ==================================================================


#= Functions & objects ========================================================
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            time.sleep(10)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()


#= Main program ===============================================================
if __name__ == '__main__':
    pass
