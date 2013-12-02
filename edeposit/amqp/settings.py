# -*- coding: utf-8 -*-
from zope import component, interface
from .config import ConnectionConfig, ExchangeConfig
from .serializers import ISerializer, DataJSONSerializer, DataJSONDeserializer, IDeserializer
from .message import IData, IDataWithUrl
from .types import IJSONString
from zope.component import getGlobalSiteManager

gsm = getGlobalSiteManager()

gsm.registerAdapter(DataJSONSerializer,(IData,),ISerializer,"messages.IData")
gsm.registerAdapter(DataJSONSerializer,(IDataWithUrl,),ISerializer,"messages.IData")
gsm.registerAdapter(DataJSONDeserializer,(IJSONString,),IDeserializer,"messages.IData")
