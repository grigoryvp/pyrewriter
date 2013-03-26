#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pyrewriter

oToken = pyrewriter.parseTxt( pyrewriter.predefined( 'nginx' ), """
        server

        {
                listen
                # some port
                80 # some comment
                # some flag
                default_server
                # token end
                ; location / { uwsgi_pass unix:/tmp/www_test.sock; }
        }
""" )
oSubToken = oToken.addChild( 'EXPR' )
oSubToken.addChild( 'CMD', 'bar' )
oSubToken.addChild( 'ARG', 42 )
oSubToken.addChild( 'TERM', ';' )

print( oToken.toStr() )

