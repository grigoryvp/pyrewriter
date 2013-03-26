#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# |Token| class that extends |pyparsing| parse results.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import info


class Token( object ) :


  def __init__(
    self,
    ##i Token name, |None| for root token.
    s_name = None,
    ##i Text, associated with token, |None| for no text.
    s_str = None ) :

    self.__lChildren = []
    self.__sName = s_name
    self.str = s_str
    ##  Contains options passed as strings into |capture|.
    self.options = {}
    ##  Contains reference to |Grammar| instance that has reference to
    ##  grammar used to produce this token and options associated with
    ##  grammar's expressions via |pyrewriter.capture|.
    self.grammar = None


  @property
  def name( self ) :
    return self.__sName


  def addChild( self, * args ) :
    assert args
    uArg = args[ 0 ]
    if isinstance( uArg, Token ) :
      assert 1 == len( args )
      oToken = uArg
    else :
      assert isinstance( uArg, basestring )
      assert len( args ) in [ 1, 2 ]
      sName = uArg
      sStr = None
      if 2 == len( args ) :
        uArg = args[ 1 ]
        assert isinstance( uArg, (basestring, int, long, float) )
        if isinstance( uArg, basestring ) :
          sStr = uArg
        else :
          sStr = str( uArg )
      oToken = Token( sName, sStr )
      oToken.grammar = self.grammar
      ##! Get options from grammar definition, if any.
      if sName in oToken.grammar.options :
        oToken.options = oToken.grammar.options[ sName ]
    self.__lChildren.append( oToken )
    return oToken


  @property
  def children( self ) :
    return self.__lChildren


  def printit( self, n_indent = 0 ) :
    sIndent = ' ' * 2 * n_indent
    print( '{0}{1}({2})'.format( sIndent, self.name, self.str ) )
    for oItem in self.__lChildren :
      oItem.printit( n_indent + 1 )


  def toStr( self, s_indent = '  ' ) :

    class Context( object ) : pass

    def recursive( o_token, n_indent, o_context ) :
      sOut = ""
      ##  Root container token?
      if None == o_token.name :
        nIndent = n_indent
      else :
        if o_token.str :
          if 'separate' in o_token.options and o_context.lastToken :
            if 'separate' in o_context.lastToken.options :
              sOut += ' '
          sOut += o_token.str
          oContext.lastToken = o_token
        if 'newline' in o_token.options :
          sOut += '\n'
        nIndent = n_indent + 1
      for oChild in o_token.children :
        sStr = recursive( oChild, nIndent, o_context )
        if sStr :
          sOut += sStr
      return sOut

    oContext = Context()
    oContext.lastToken = None
    return recursive( self, 0, oContext )

