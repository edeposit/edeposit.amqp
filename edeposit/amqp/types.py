# -*- coding: utf-8 -*-
from zope import interface, schema, component
from gettext import gettext as _

TypeOfSerialization = (
    'JSON',
    'BSON',
    'XML',
    'Protobuf'
)

InterfaceOfData = (
    'antivir.check',
    'aleph.search',
    'pdfbox.validate',
    'pdfbox.validateAndExtractMetadata',
    'pdfbox.extractMetadata',
    'epubcheck.validate',
    'epubcheck.validateAndExtractMetadata',
    'epubcheck.extractMetadata',
)


class IJSONString(interface.Interface):
    """ marker interface for string containg json data """
    stream = schema.ASCII(
        title = _(u'data of a string'),
        description = _(u''),
    )
    pass


class JSONString(object):
    interface.implements(IJSONString)

    def __init__(self, stream):
        self.stream = stream


