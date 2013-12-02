# -*- coding: utf-8 -*-
from zope import component, interface
from .config import ConnectionConfig, ExchangeConfig
from .serializers import ISerializer, SimpleJSONSerializer, SimpleJSONDeserializer, IDeserializer
from .message import IData, IDataWithUrl
from .types import IStringStream
from zope.component import getGlobalSiteManager

gsm = getGlobalSiteManager()

gsm.registerAdapter(SimpleJSONSerializer,(IData,),ISerializer,"json")
gsm.registerAdapter(SimpleJSONSerializer,(IDataWithUrl,),ISerializer,"json")
gsm.registerAdapter(SimpleJSONDeserializer,(IStringStream,),IDeserializer,"json")
