#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pyrewriter


oToken = pyrewriter.parse( 'nginx', '''
  http {
    server {
      location / {
        uwsgi_pass unix:/tmp/www_test.sock;
      }
    }
  }
''' )
sQuery =  '/EXPR/CMD=http,BLOCK/(EXPR)/CMD=server,BLOCK'
sQuery += '/EXPR/CMD=location,BLOCK/EXPR/CMD=uwsgi_pass'
sQuery += ',ARG=\'unix:/tmp/www_test.sock\''
assert oToken.searchOne( sQuery )

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
oToken.addChild( pyrewriter.parse( 'nginx', """
  foo {
    bar "#";
    baz 2;
  }
""" ).children().first() )
oToken.addChild( s_raw = """
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

oToken = pyrewriter.parse( 'nginx', """
  server {
    name "foo";
  } # terminator
  # after block
""" )
if oToken.child( 'FOO' ) :
  pass
else :
  oBlock = oToken.child( 'EXPR' ).child( 'BLOCK' ).child( 'BLOCK_END' )
  oBlock.addSiblingBefore( s_raw = "foo 1;" )
  oBlock = oToken.child( 'EXPR' ).child( 'BLOCK' ).child( 'BLOCK_BEGIN' )
  oBlock.addSiblingAfter( s_raw = "foo2 2; foo3 3;" )

oToken = pyrewriter.parse( 'nginx', 'a 1; b 2;' )
oToken.child( 'EXPR' ).replace( s_raw = 'foo 2;' )

oToken = pyrewriter.parse( 'nginx', '''
  foo;
''' )
assert oToken.searchOne( "/(EXPR)/CMD=foo" ).name == 'EXPR'
assert oToken.search( "/EXPR/(CMD=foo)" ).first().val == 'foo'

oToken = pyrewriter.parse( 'nginx', '''
  foo / {
    bar 2;
    baz 3;
  }
''' )
assert oToken.search( "/EXPR/CMD,(ARG)" ).first().val == '/'
assert oToken.search( "/EXPR/CMD=foo,BLOCK/EXPR/(ARG)" ).last().val == '3'

oToken = pyrewriter.parse( 'nginx', '''
  http {
    server_names_hash_bucket_size true;
  }
''' )
sQuery = '/EXPR/CMD=http,BLOCK/EXPR/(CMD=server_names_hash_bucket_size)'
assert oToken.searchOne( sQuery ).val == 'server_names_hash_bucket_size'

