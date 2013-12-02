# -*- coding: utf-8 -*-
from zope import interface, component, schema
from collections import namedtuple
import gettext
_ = gettext.gettext

class IConnectionConfig(interface.Interface):
    url = schema.ASCIILine(
        title = _(u'url of RabbitMQ vhost'),
        description = _(u'example: amqp://guest@guest:localhost:5672/vhost/'),
        required = True,
        )

class IExchangeConfig(interface.Interface):
    name = schema.ASCIILine(
        title = _(u'name of exchange'),
        required = True,
    )
    type = schema.ASCIILine(
        title = _(u'type of exchange'),
        description = _(u'choose one of: fanout, direct, topics'),
        required = True,
    )
    durable = schema.Bool(
        title = _(u'Is durable?'),
        description = _(u'Is exchang durable?'),
        required = True,
    )


class ConnectionConfig(namedtuple('AMQPVhostVonnectionConfig',['url',])):
    interface.implements(IConnectionConfig)
    pass

class ExchangeConfig(namedtuple('AMQPExchangeConfig',['name','type','durable'])):
    interface.implements(IExchangeConfig)
    pass
