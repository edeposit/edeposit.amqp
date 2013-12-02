# -*- coding: utf-8 -*-
from zope import interface, component
from kombu import Connection, Exchange
from .config import IConnectionConfig, IExchangeConfig

class IDataExecutor(interface.Interface):
    def execute(data, deliveryMetadata, metadata):
        """ it will do something with request message. It returns new message with result of an handler.
        The result will be sent by other interface.
        """

class ISender(interface.Interface):
    def send(message):
        """ the message will be sent.
        Message will be adapted to:
        - IDeliveryMetadata to get delivery informations
        - IMetadata to get headers of a message
        - ISerializer to serialize it

        And sent to a queue. Each instance will know what exchange uses.
        """


class SimpleTestSender(object):
    interface.implements(ISender)

class AMQPSimpleExchangeSender(object):
    interface.implements(ISender)

    def __init__(self, connectionConfig, exchangeConfig):
        self.exchangeConfig = exchangeConfig
        self.connectionConfig = connectionConfig
        self.url = IConnectionConfig(self.connectionConfig).url
        self.exchange = Exchange( IExchangeConfig(exchangeConfig).name,
                                  type = IExchangeConfig(exchangeConfig).type,
                                  durable = IExchangeConfig(exchangeConfig).durable)

    def send(message):
        """ it will send data to AMQPExchange """
        with Connection(self.url) as conn:
            producer = conn.Producer()
            producer.publish(data, headers = headers, exchange = self.exchange)
            pass
