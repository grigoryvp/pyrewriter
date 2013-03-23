#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library core.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import inspect
import imp
import os

from token import Token

class Context( object ) :


  __oInst = None


  def __init__( self ) :
    self.predefined = {}


  @classmethod
  def get( self ) :
    if not self.__oInst :
      self.__oInst = Context()
    return self.__oInst


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


def predefined( s_name ) :
  if s_name not in Context.get().predefined :
    sModule = 'predefined_{0}'.format( s_name )
    sFile = '{0}.py'.format( sModule )
    sDir = os.path.dirname( os.path.abspath( __file__ ) )
    sPath = os.path.join( sDir, sFile )
    Context.get().predefined[ s_name ] = imp.load_source( sModule, sPath )
  return Context.get().predefined[ s_name ].GRAMMAR


def parseTxt( o_grammar, s_txt ) :
  ##  Root token.
  oToken = Token()
  for oSubtoken in o_grammar.parseString( s_txt ) :
    oToken.addChild( oSubtoken )
  return oToken

