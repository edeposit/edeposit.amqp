# -*- coding: utf-8 -*-
import unittest
from zope import interface, component
from zope.component import getAdapter

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_of_imports(self):
        from edeposit.amqp import message, actors, config
        from edeposit.amqp import settings
        from edeposit.amqp import serializers

    def test_interfaces(self):
        from edeposit.amqp import message, actors, config
        from edeposit.amqp import settings

        connectionConfig = config.ConnectionConfig(url="amqp://guest@guest:localhost/vhost/")
        self.assertTrue(config.IConnectionConfig.providedBy(connectionConfig), 
                        "ConnectionConfig provides IConnectionConfig interface")
        self.assertTrue(connectionConfig.url)
        exchangeConfig = settings.ExchangeConfig(name='search',
                                                 type='fanout',
                                                 durable=True)
        self.assertTrue(exchangeConfig.name)
        self.assertTrue(exchangeConfig.type)
        self.assertTrue(exchangeConfig.durable)
        self.assertTrue(config.IExchangeConfig.providedBy(exchangeConfig),
                        "exchange config provides IExchangeConfig interface")
        
    def test_message_interfaces(self):
        from edeposit.amqp import message, actors, config
        from edeposit.amqp import settings
        data = message.Data(uuid="uuid")
        self.assertTrue(message.IData.providedBy(data))
        self.assertTrue(data.uuid=='uuid')

        dataWithStream = message.DataWithStream(stream="stream")
        self.assertTrue(dataWithStream.uuid)
        self.assertTrue(dataWithStream.stream=="stream")
        dataWithStream = message.DataWithStream(uuid="uuid")
        dataWithStream = message.DataWithStream(uuid="uuid",stream="stream")
        self.assertTrue(dataWithStream.uuid=="uuid")
        self.assertTrue(dataWithStream.stream=="stream")

        dataWithRelation = message.DataWithRelation(relatedUUID="related uuid")
        self.assertTrue(dataWithRelation.uuid)
        self.assertTrue(dataWithRelation.uuidOfParent=="related uuid")
        dataWithRelation = message.DataWithRelation(uuid="uuid", relatedUUID="related uuid")
        self.assertTrue(dataWithRelation.uuid=="uuid")
        self.assertTrue(dataWithRelation.uuidOfParent=="related uuid")

        dataWithUrl = message.DataWithUrl(url="url")
        self.assertTrue(dataWithUrl.uuid)
        self.assertTrue(dataWithUrl.url=="url")
        dataWithUrl = message.DataWithUrl(uuid="uuid", url="url")
        self.assertTrue(dataWithUrl.uuid=="uuid")
        self.assertTrue(dataWithUrl.url=="url")
    
    def test_sender(self):
        from edeposit.amqp import actors, config, message
        from edeposit.amqp import settings

        connectionConfig = config.ConnectionConfig(url="amqp://guest@guest:localhost/vhost/")
        exchangeConfig = config.ExchangeConfig(name='search',
                                                 type='fanout',
                                                 durable=True)
        sender = actors.AMQPSimpleExchangeSender(connectionConfig, exchangeConfig)
        

    def test_serializer_import(self):
        from edeposit.amqp import actors, config, message
        from edeposit.amqp import settings
        from edeposit.amqp import serializers

    def test_serializer_adapters(self):
        from edeposit.amqp import actors, config, message, types
        from edeposit.amqp import settings
        from edeposit.amqp import serializers
        
        data = message.Data()
        serializer = getAdapter(data,serializers.ISerializer,'messages.IData')
        stream = serializer.serialize()

        stream = types.JSONString(stream=stream)
        deserializer = getAdapter(stream, serializers.IDeserializer,'messages.IData')
        data = deserializer.deserialize()
