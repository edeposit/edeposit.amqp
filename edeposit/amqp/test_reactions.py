#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 Unported License
# (http://creativecommons.org/licenses/by/3.0/).
#
#= Imports ====================================================================
import aleph
import aleph.convertors


#= Main program ===============================================================
if __name__ == '__main__':
    isbnq = aleph.ISBNQuery("80-251-0225-4")
    request = aleph.SearchRequest(isbnq, "trololo")

    json = aleph.convertors.toJSON(request)

    aleph.convertors.fromJSON(json)

    print json
