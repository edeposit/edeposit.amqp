from .interfaces import *
from zope import interface, component
from pika import 

@interface.implementer(IResponseSender)
class AMQPSimpleSender(object):
    def __init__(self, msg):
        self.msg = msg
        
    def send():
        """ it will send to AMQPChannel with the same name as interface of an message """
        response = IResponse(self.msg)
        interfaceOfMSG = response.interfaceOfMsg
        channel = component.queryUtility(IAMQPChannel, interfaceOfMSG)
        channel.publish(response)
