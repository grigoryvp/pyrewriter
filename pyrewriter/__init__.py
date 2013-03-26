#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Rewriter Library core.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import inspect
import imp
import os

from token import Token
import info
import grammar


##  List of valid token options that can be passed to |capture|.
ABOUT_OPTIONS = [ 'newline', 'separate' ]


class Context( object ) :


  __oInst = None


  def __init__( self ) :
    self.predefined = {}


  @classmethod
  def get( self ) :
    if not self.__oInst :
      self.__oInst = Context()
    return self.__oInst


def capture( o_expr, * args ) :

  mLocals = inspect.currentframe().f_back.f_locals
  for sId in mLocals :
    if id( mLocals[ sId ] ) == id( o_expr ) :
      sName = sId
      break
  else :
    assert False, "Object without identifier passed to Capture()"

  mOptions = {}
  for sOption in args :
    assert sOption in ABOUT_OPTIONS
    mOptions[ sOption ] = True

  def parseAction( s_txt, n_pos, o_token ) :
    oToken = Token( sName )
    for oChild in [ o for o in o_token if isinstance( o, Token ) ] :
      oToken.addChild( oChild )
    lTxt = [ o for o in o_token if isinstance( o, basestring ) ]
    assert len( lTxt ) < 2
    if lTxt :
      oToken.str = lTxt[ 0 ]
      oToken.options.update( mOptions )
    return oToken
  o_expr.addParseAction( parseAction )

  if not hasattr( o_expr, info.CTX_NAME ) :
    setattr( o_expr, info.CTX_NAME, { 'options': mOptions } )
  else :
    assert False, "Single object captured more than once"


def predefined( s_name ) :
  if s_name not in Context.get().predefined :
    sModule = 'predefined_{0}'.format( s_name )
    sFile = '{0}.py'.format( sModule )
    sDir = os.path.dirname( os.path.abspath( __file__ ) )
    sPath = os.path.join( sDir, sFile )
    Context.get().predefined[ s_name ] = imp.load_source( sModule, sPath )
  return Context.get().predefined[ s_name ].GRAMMAR


##x Evaluates to root unnamed token that contains top-level tokens produced
##  by applying grammar to text.
##! Must be used instead of calling |grammar.parseString| since it also
##  adds reference to grammar into tokens that is required for some
##  mechanics to work.
def parseTxt( o_grammar, s_txt ) :
  ##  Root token.
  oToken = Token()
  ##  Grammar definition.
  oGrammar = grammar.Grammar()
  oGrammar.root = o_grammar
  for oSubtoken in o_grammar.parseString( s_txt ) :
    oToken.addChild( oSubtoken )
  def recursiveSetGrammar( o_token ) :
    o_token.grammar = oGrammar
    for oChild in o_token.children :
      recursiveSetGrammar( oChild )
  recursiveSetGrammar( oToken )
  return oToken

