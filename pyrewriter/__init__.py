#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library core.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import inspect

from token import Token


def capture( o_expr ) :
  mLocals = inspect.currentframe().f_back.f_locals
  for sId in mLocals :
    if id( mLocals[ sId ] ) == id( o_expr ) :
      sName = sId
      break
  else :
    assert False, "Object without name passed to Capture()"
  def parseAction( s_txt, n_pos, o_token ) :
    oToken = Token( sName )
    for oChild in [ o for o in o_token if isinstance( o, Token ) ] :
      oToken.addChild( oChild )
    lTxt = [ o for o in o_token if isinstance( o, basestring ) ]
    assert len( lTxt ) < 2
    if lTxt :
      oToken.txt = lTxt[ 0 ]
    return oToken
  o_expr.addParseAction( parseAction )


def parseTxt( o_grammar, s_txt ) :
  ##  Root token.
  oToken = Token()
  for oSubtoken in o_grammar.parseString( s_txt ) :
    oToken.addChild( oSubtoken )
  return oToken

