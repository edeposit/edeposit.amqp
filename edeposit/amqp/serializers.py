# -*- coding: utf-8 -*-
from zope import interface, component
import simplejson
from edeposit.amqp import message
from edeposit.amqp import types

class ISerializer(interface.Interface):
    
    def serialize():
        """ return serialized data """
        pass

class IDeserializer(interface.Interface):
    
    def deserialize():
        """ return serialized data """
        pass

class DataJSONSerializer(object):
    interface.implements(ISerializer)
    component.adapts(message.IData)
    
    def __init__(self, data):
        self.data = data

    def serialize(self):
        return simplejson.dumps({'uuid': str(self.data.uuid)})


class DataJSONDeserializer(object):
    interface.implements(IDeserializer)
    component.adapts(types.IJSONString)
    
    def __init__(self, stream):
        self.stream = stream

    def deserialize(self):
        data = simplejson.loads(self.stream.stream)
        return message.Data(uuid=data)
