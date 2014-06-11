#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
ProFTPD log monitor. This script reacts to preprogrammed events generated by
ProFTPD server. Look at :mod:`ftp.monitor` for details.
"""
# Imports =====================================================================
import os
import sys
import uuid
import os.path
import argparse
import traceback

import sh
import pika
from pika.exceptions import ConnectionClosed

from edeposit.amqp.ftp import reactToAMQPMessage, monitor
from edeposit.amqp.ftp.settings import LOG_FILE
from edeposit.amqp.ftp.structures import *  # for serializers
from edeposit.amqp.ftp.monitor import process_log, _read_stdin

import edeposit.amqp.serializers as serializers


# if the amqp module wasn't yet installed at this system, load it from package
try:
    from edeposit.amqp import settings
except ImportError:
    sys.path.insert(0, os.path.abspath('../edeposit/'))
    import amqp
    sys.modules["edeposit.amqp"] = amqp

from edeposit.amqp import settings
from edeposit.amqp.amqpdaemon import AMQPDaemon, getConParams


# Functions & objects =========================================================
class FTPMonitorDaemon(AMQPDaemon):
    """
    This daemon monitors events at FTP server and sends messages to output
    queue.
    """
    def __init__(self, con_param, queue, out_exch, out_key, react_fn, glob, fn):
        """
        Args:
            con_param (ConnectionParameters): See :func:`.getConParams` for
                                              details.
            queue (str):    Name of the input queue.
            out_exch (str): Name of the exchange for outgoing messages.
            out_key (str):  What key will be used to send messages back.
            react_fn (fn):  Not used in this case. Set to None.
            glob (dict):    Result of ``globals()`` call - used in deserializer
                            to automatically build classes, which are not
                            available in this namespace of this package.
            fn (str):       Extended log filename.
        .
        """
        super(FTPMonitorDaemon, self).__init__(
            con_param=con_param,
            queue=queue,
            out_exch=out_exch,
            out_key=out_key,
            react_fn=None,
            glob=glob
        )
        self.ftp_extended_log = fn

    def body(self):
        """
        This method handles AMQP connection details and reacts to FTP events by
        sending messages to output queue.
        """
        self.connection = pika.BlockingConnection(self.connection_param)
        self.channel = self.connection.channel()

        print "Monitoring file '%s'." % self.ftp_extended_log

        file_iter = process_log(
            sh.tail("-f", self.ftp_extended_log, _iter=True)
        )
        for import_request in file_iter:
            self.sendMessage(
                exchange=self.output_exchange,
                routing_key=self.output_key,
                message=serializers.serialize(import_request),
                UUID=str(uuid.uuid1())
            )


def main(args, stop=False):
    """
    Arguments parsing, etc..
    """
    if not stop and not os.path.exists(args.filename):
        sys.stderr.write("'%s' doesn't exists!\n" % args.filename)
        sys.exit(1)

    daemon = FTPMonitorDaemon(
        con_param=getConParams(
            settings.RABBITMQ_FTP_VIRTUALHOST
        ),
        queue=settings.RABBITMQ_FTP_INPUT_QUEUE,
        out_exch=settings.RABBITMQ_FTP_EXCHANGE,
        out_key=settings.RABBITMQ_FTP_OUTPUT_KEY,
        react_fn=None,
        glob=globals(),               # used in deserializer
        fn=args.filename if not stop else ""
    )

    if not stop and args.foreground:  # run at foreground
        daemon.run()
    else:
        daemon.run_daemon()           # run as daemon


# Main program ================================================================
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        main(None, stop=True)
        sys.exit(0)

    parser = argparse.ArgumentParser(
        usage='%(prog)s start/stop/restart [-f] FN',
        description="""ProFTPD log monitor. This script reacts to preprogrammed
                       events from FTP server."""
    )
    parser.add_argument(
        "-f",
        '--foreground',
        action="store_true",
        required=False,
        help="""Run at foreground, not as daemon. If not set, script is will
                run at background as unix daemon."""
    )
    parser.add_argument(
        "-n",
        "--filename",
        required=True,
        type=str,
        help="Path to the log file (usually " + LOG_FILE + ")."
    )
    parser.add_argument(
        "action",
        metavar="start/stop/restart",
        type=str,
        default=None,
        help="Start/stop/restart the daemon."
    )
    args = parser.parse_args()

    try:
        main(args)
    except ConnectionClosed as e:
        sys.stderr.write(
            e.message +
            "\nConnectionClosed: Are the RabbitMQ queues properly set?\n"
        )
        sys.exit(1)
    except KeyboardInterrupt:
        pass
