#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# |Token| class that extends |pyparsing| parse results.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import info
import parse
import predefined


class Token( object ) :


  def __init__(
    self,
    ##i Token name, |None| for root token.
    s_name = None,
    ##i Text, associated with token, |None| for no text.
    s_val = None ) :

    self.__lChildren = []
    self.__sName = s_name
    self.val = s_val
    ##  Contains options passed as strings into |capture|.
    self.options = {}
    ##  Contains reference to |Grammar| instance that has reference to
    ##  grammar used to produce this token and options associated with
    ##  grammar's expressions via |pyrewriter.capture|.
    self.grammar = None


  @property
  def name( self ) :
    return self.__sName


  @property
  def children( self ) :
    return self.__lChildren


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
      sVal = None
      if 2 == len( args ) :
        uArg = args[ 1 ]
        assert isinstance( uArg, (basestring, int, long, float) )
        if isinstance( uArg, basestring ) :
          sVal = uArg
        else :
          sVal = str( uArg )
      oToken = Token( sName, sVal )
      oToken.grammar = self.grammar
      ##! Get options from grammar definition, if any.
      if sName in oToken.grammar.options :
        oToken.options = oToken.grammar.options[ sName ]
    self.__lChildren.append( oToken )
    return oToken


  def addChildFromStr( self, s_child ) :
    oRoot = parse.parseStr( self.grammar.root, s_child )
    for oToken in oRoot.children :
      self.addChild( oToken )

  def printit( self, n_indent = 0 ) :
    sIndent = ' ' * 2 * n_indent
    print( '{0}{1}({2})'.format( sIndent, self.name, self.val ) )
    for oItem in self.__lChildren :
      oItem.printit( n_indent + 1 )


  def toStr( self, s_indent = '  ' ) :

    class Context( object ) : pass

    def recursive( o_token, o_context ) :
      ##! Token like '}' unidents itself.
      if 'unindent' in o_token.options :
        assert o_context.indent > 0, "Mismatched umber of { and }"
        o_context.indent -= 1
      if o_token.val :
        ##  Not a first token on the line?
        if o_context.out and not o_context.out.endswith( '\n' ) :
          if o_context.lastToken :
            if 'separate' in o_token.options :
              if 'separate' in o_context.lastToken.options :
                  o_context.out += ' '
        ##  First token in the line?
        else :
          o_context.out += o_context.indent * s_indent
        o_context.out += o_token.val
        oContext.lastToken = o_token
      if 'newline' in o_token.options :
        o_context.out += '\n'
      if 'indent' in o_token.options :
        o_context.indent += 1
      for oChild in o_token.children :
        recursive( oChild, o_context )

    oContext = Context()
    oContext.lastToken = None
    oContext.indent = 0
    oContext.out = ""
    recursive( self, oContext )
    return oContext.out


  def findChild( self, s_name, s_val = None ) :

    lFound = []

    def recursive( o_token, l_found ) :
      if s_name == o_token.name and (not s_val or s_val == o_token.val) :
        l_found.append( o_token )
      for oToken in o_token.children :
        recursive( oToken, l_found )

    for oToken in self.children :
      recursive( oToken, lFound )
    return lFound

