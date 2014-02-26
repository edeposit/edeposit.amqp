Introduction
============
This module contains common parts shared with other AMQP modules from edeposit
project.

Specifically, there is:

Modules
=======
edeposit.amqp.settings
----------------------
Configuration for RabbitMQ server and edeposit client modules connecting into it.

edeposit.amqp.daemonwrapper
---------------------------
Class for spawning true unix daemons.

edeposit.amqp.pikadaemon
------------------------
Generic AMQP blocking communication daemon server.

Scripts
=======
edeposit/amqp/alephdaemon.py
-------------------------
Daemon providing AMQP communication with the [Aleph module](https://github.com/jstavel/edeposit.amqp.aleph).

edeposit/amqp/amqp_tool.py
--------------------------
Script for testing the communication and creating exchanges/queues/routes in RabbitMQ.