# -*- coding: utf-8 -*-
from zope import interface, component, schema
from collections import namedtuple
import uuid as UUID

import gettext
_ = gettext.gettext

class IData(interface.Interface):
    uuid = schema.ASCIILine(
        title = _(u'UUID of a Response'),
        description = _(u'Unique number of a response message'),
        required = True,
        )
    pass

class IMetadata(interface.Interface):
    contentType = schema.ASCIILine(
        title = _(u'Interface describing msg attribute'),
        description = _(u'Message wears inner msg (see attribute msg). The msg has its own interface.'),
        required = True,
        )

    uuid = schema.ASCIILine(
        title = _(u'UUID of a Response'),
        description = _(u'Unique number of a response message'),
        required = True,
        )

    created = schema.Datetime(
        title = _(u'Date time when Response was created at.'),
        description = _(u''),
        required = True,
        )

class IEncodingMetadata(interface.Interface):
    contentEncoding = schema.ASCIILine(
        title = _(u'Serialization interface'),
        description = _(u'What way was msg attribute serialized.'),
        required = True,
        )

class IDeliveryMetadata(interface.Interface):
    deliveryMode = schema.ASCIILine(
        title = _(u'Delivery mode for AMQP Message'),
        description = _(u''),
        required = True,
        )

    replyTo = schema.ASCIILine(
        title = _(u'Reply to for AMQP Message'),
        description = _(u''),
        required = True,
        )

    routingKey = schema.ASCIILine(
        title = _(u'Routing key for AMQP Message'),
        description = _(u''),
        required = True,
        )
    
class IDataWithStream(IData):
    stream = schema.Bytes(
        title = _(u'Stream with data'),
        description = _(u''),
        required = True,
    )

class IDataWithUrl(IData):
    url = schema.URI(
        title = _(u'Url'),
        description = _(u''),
        required = True,
    )

class IDataWithValidationResult(IData):
    isValid = schema.Bool(
        title = _(u'Is valid?'),
        description = _(u''),
        required = True,
    )
    errors = schema.ASCII(
        title = _(u'errors'),
        description = _(u''),
        required = False,
    )
    message = schema.ASCII(
        title = _(u'Result message'),
        description = _(u'Message with more informations about result'),
        required = False,
    )

class IDataWithRelation(IData):
    uuidOfParent = schema.ASCII(
        title = _(u'UUID of parent'),
        description = _(u'UUID of a data that are with relation to this data.'),
        required = True,
    )

class Data(object):
    interface.implements(IData)

    def __init__(self, uuid=None):
        self.uuid = uuid or UUID.uuid4()

class DataWithStream(Data):
    interface.implements(IDataWithStream)

    def __init__(self, uuid=None, stream=None):
        Data.__init__(self,uuid=uuid)
        self.stream = stream


class DataWithRelation(Data):
    interface.implements(IDataWithRelation)

    def __init__(self, uuid=None, relatedUUID = None):
        Data.__init__(self, uuid=uuid)
        self.uuidOfParent = relatedUUID
    

class DataWithUrl(Data):
    interface.implements(IDataWithUrl)

    def __init__(self, uuid=None, url = None):
        Data.__init__(self, uuid=uuid)
        self.url = url
    
