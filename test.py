#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pyrewriter

oToken = pyrewriter.parseTxt( pyrewriter.predefined( 'nginx' ), """
  foo "1";
  bar ab; # comment
""" )
oSubToken = oToken.addChild( 'EXPR' )
oSubToken.addChild( 'CMD', 'bar' )
oSubToken.addChild( 'ARG', 42 )
oSubToken.addChild( 'TERM', ';' )
pyrewriter.predefined( 'nginx' )

