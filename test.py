#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

from pyrewriter import cfg_nginx

lTokens = cfg_nginx.GRAMMAR.parseString( """
  foo "1";
  bar baz; # comment
""" )
for oToken in lTokens :
  oToken.printit()

