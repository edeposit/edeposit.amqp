# -*- coding: utf-8 -*-
from zope import interface, component, schema
import gettext
_ = gettext.gettext

class IResponse(interface.Interface):
    uuid = schema.ASCIILine(
        title = _(u'UUID of a Response'),
        description = _(u'Unique number of a response message'),
        required = True,
        )
    
    uuidOfRequest = schema.ASCIILine(
        title = _(u'UUID of Request'),
        description = _(u'Unique number of a Request that the response responses to.'),
        required = True,
        )

    created = schema.Datetime(
        title = _(u'Date time when Response was created at.'),
        description = _(u''),
        required = True,
        readonly = False,
        )
    
    interfaceOfMsg = schema.ASCIILine(
        title = _(u'Interface describing msg attribute'),
        description = _(u'Request message wears inner msg (see attribute msg). The msg has its own interface.'),
        required = False,
        )

    serializationOfMsg = schema.ASCIILine(
        title = _(u'Serialization interface'),
        description = _(u'What way was msg attribute serialized.'),
        required = True,
        )
    
    msg = schema.Bytes(
        title = _(u'Inner message'),
        description = _(u'Message that wears main information for consuments.'),
        required = True,
        )


class IRequest(interface.Interface):
    uuid = schema.ASCIILine(
        title = _(u'UUID of a request'),
        description = _(u'Unique number of a request message'),
        required = True,
        )
    
    created = schema.Datetime(
        title = _(u'Date time when Request was created at.'),
        description = _(u''),
        required = True,
        readonly = False,
        )
    
    interfaceOfMsg = schema.ASCIILine(
        title = _(u'Interface describing msg attribute'),
        description = _(u'Request message wears inner msg (see attribute msg). The msg has its own interface.'),
        required = False,
        )

    serializationOfMsg = schema.ASCIILine(
        title = _(u'Serialization interface'),
        description = _(u'What way was msg attribute serialized.'),
        required = True,
        )
    
    msg = schema.Bytes(
        title = _(u'Inner message'),
        description = _(u'Message that wears main information for consuments.'),
        required = True,
        )
    


class IRequestHandler(interface.Interface):
    request = interface.Attribute("request to be handled")

    def handle():
        """ it will do something with request message. It returns new message with result of an handler.
        The result will be sent by other interface.
        """

class IMessageSender(interface.Interface):
    msg = interface.Attribute("message to be sent")
    def send():
        """ the response will be sent.
        Message will be casted to an IResponse interface.o
        """
        
    
