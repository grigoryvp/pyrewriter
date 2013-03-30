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
""" ).children().first() )
oToken.addChildFromStr( """
  foo {
    bar "#";
    baz 2;
  }
""" )

##  Simple modification.
for oItem in oToken.descendants( 'CMD', 'foo' ) :
  oBlock = oItem.siblings( 'BLOCK' ).first()
  oVal = oBlock.descendants( 'CMD', 'baz' ).first().siblings( 'ARG' ).first()
  oVal.val = '3'

oToken = pyrewriter.parse( pyrewriter.predefined( 'nginx' ), """
  server {
    name "foo";
  } # terminator
  # after block
""" )
oBlock = oToken.child( 'EXPR' ).child( 'BLOCK' ).child( 'BLOCK_END' )
oBlock.addSiblingBeforeFromStr( "foo = 1;" )
print( oToken.toStr() )

