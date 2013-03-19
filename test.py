#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

from pyrewriter import cfg_nginx, Token, parseTxt

oToken = parseTxt( cfg_nginx.GRAMMAR, """
  foo "1";
  bar ab; # comment
""" )
oToken = Token( 'EXPR' )
oToken.addChild( Token( 'CMD', 'bar' ) )
oToken.addChild( Token( 'ARG', '42' ) )
oToken.addChild( Token( 'TERM', ';' ) )

