# -*- coding: utf-8 -*-
class IValues(interface.Interface):
    uuid = schema.ASCIILine(
        title = _(u'UUID of a Response'),
        description = _(u'Unique number of a response message'),
        required = True,
        )
    
    created = schema.Datetime(
        title = _(u'Date time when Response was created at.'),
        description = _(u''),
        required = True,
        readonly = False,
        )

    interface = schema.ASCIILine(
        title = _(u'Interface describing msg attribute'),
        description = _(u'Message wears inner msg (see attribute msg). The msg has its own interface.'),
        required = False,
        )

