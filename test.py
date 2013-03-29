#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pyrewriter

oToken = pyrewriter.parse( pyrewriter.predefined( 'nginx' ), """
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
oToken.addChild( pyrewriter.parse( pyrewriter.predefined( 'nginx' ), """
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

##  Simple modification.
for oItem in oToken.findChild( 'CMD', 'foo' ) :
  oBlock = oItem.findSibling( 'BLOCK' )[ 0 ]
  oVal = oBlock.findChild( 'CMD', 'baz' )[ 0 ].findSibling( 'ARG' )[ 0 ]
  oVal.val = '3'

print( oToken.toStr() )

