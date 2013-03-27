#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pyrewriter

oToken = pyrewriter.parseStr( pyrewriter.predefined( 'nginx' ), """
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
oToken.addChild( pyrewriter.parseStr( pyrewriter.predefined( 'nginx' ), """
  foo {
    bar "#";
    baz 2;
  }
""" ).children[ 0 ] )
oToken.addChildFromStr( """
  foo {
    bar "#";
    baz 2;
  }
""" )

for oItem in oToken.findChild( 'CMD', 'foo' ) :
  pass
  # oBlock = oItem.findSibling( 'BLOCK' )[ 0 ]

print( oToken.toStr() )

