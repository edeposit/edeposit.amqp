# -*- coding: utf-8 -*-
from zope import interface, component, schema
import gettext
_ = gettext.gettext

class IResponse(interface.Interface):
    uuid = schema.ASCIILine(
        title = _(u'UUID of a request'),
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


