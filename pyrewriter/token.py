#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# |Token| class that extends |pyparsing| parse results.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import info
import parse
import predefined


class ListEx( list ) :


  def first( self ) :
    return self[ 0 ]


  def last( self ) :
    return self[ -1 ]


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
    ##  Reference to parent token, None if this is root token.
    self.parent = None
    ##  Reference to result of last |find...| command.
    self.found = ListEx()


  @property
  def name( self ) :
    return self.__sName


  def addChild( self, * args, ** kwargs ) :
    for oToken in self.__tokensFromArgs( * args, ** kwargs ) :
      oToken.parent = self
      self.__lChildren.append( oToken )
    return oToken


  def addChildFromStr( self, s_child ) :
    oRoot = parse.parse( self.grammar.root, s_child )
    for oToken in oRoot.children() :
      self.addChild( oToken )


  def addSiblingBefore( self, * args, ** kwargs ) :
    assert self.parent
    for nChild, oChild in enumerate( self.parent.__lChildren ) :
      if oChild == self :
        lTokens = self.__tokensFromArgs( * args, ** kwargs )
        for nToken, oToken in enumerate( lTokens ) :
          oToken.parent = self.parent
          self.parent.__lChildren.insert( nChild + nToken, oToken )
        break
    else :
      assert False, "internal consistency error"
    return oToken


  def addSiblingBeforeFromStr( self, s_child ) :
    oRoot = parse.parse( self.grammar.root, s_child )
    for oToken in oRoot.children() :
      self.addSiblingBefore( oToken )


  def addSiblingAfter( self, * args, ** kwargs ) :
    assert self.parent
    for nChild, oChild in enumerate( self.parent.__lChildren ) :
      if oChild == self :
        lTokens = self.__tokensFromArgs( * args, ** kwargs )
        for nToken, oToken in enumerate( lTokens ) :
          oToken.parent = self.parent
          self.parent.__lChildren.insert( nChild + nToken + 1, oToken )
        break
    else :
      assert False, "internal consistency error"
    return oToken


  def addSiblingAfterFromStr( self, s_child ) :
    oRoot = parse.parse( self.grammar.root, s_child )
    for oToken in oRoot.children() :
      self.addSiblingAfter( oToken )


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
      for oChild in o_token.children() :
        recursive( oChild, o_context )

    oContext = Context()
    oContext.lastToken = None
    oContext.indent = 0
    oContext.out = ""
    recursive( self, oContext )
    return oContext.out


  def __repr__( self ) :

    class Context( object ) : pass

    def recursive( o_token, o_context ) :
      if o_context.out :
        o_context.out += '\n'
      o_context.out += '  ' * o_context.indent
      o_context.out += '{0}( {1} )'.format( o_token.name, o_token.val )
      o_context.indent += 1
      for oChild in o_token.children() :
        recursive( oChild, o_context )
      o_context.indent -= 1

    oContext = Context()
    oContext.indent = 0
    oContext.out = ""
    recursive( self, oContext )
    return oContext.out


  def __descendants( self, s_name, s_val = None, f_recursive = True ) :

    lFound = []

    def recursive( o_token, l_found ) :
      if s_name == o_token.name and (not s_val or s_val == o_token.val) :
        l_found.append( o_token )
      if f_recursive :
        for oToken in o_token.children() :
          recursive( oToken, l_found )

    for oToken in self.children() :
      recursive( oToken, lFound )
    self.found = ListEx( lFound )
    return self.found


  def children( self, s_name = None, s_val = None ) :
    if not s_name :
      return ListEx( self.__lChildren )
    return self.__descendants( s_name, s_val, f_recursive = False )


  def child( self, s_name = None, s_val = None ) :
    lChildren = self.children( s_name, s_val )
    if lChildren :
      self.found = lChildren[ 0 ]
    else :
      self.found = None
    return self.found


  def setChildren( self, l_children ) :
    self.__lChildren = l_children


  def descendants( self, s_name, s_val = None ) :
    return self.__descendants( s_name, s_val, f_recursive = True )


  def descendant( self, s_name, s_val = None ) :
    lDescendants = self.descendants( s_name, s_val )
    if lDescendants :
      self.found = lDescendants[ 0 ]
    else :
      self.found = None
    return self.found


  def siblings( self, s_name, s_val = None ) :
    if self.parent :
      return self.parent.__descendants( s_name, s_val, f_recursive = False )
    return ListEx()


  def sibling( self, s_name, s_val = None ) :
    lSiblings = self.siblings( s_name, s_val )
    if lSiblings :
      self.found = lSiblings[ 0 ]
    else :
      self.found = None
    return self.found


  ##x Used by |addChild|, |addSibling| etc. Creates token from args that
  ##  can be token, one string for name, string and other value for name
  ##  and val, |s_raw| keywoard arg for raw text token representation that
  ##  need to be parsed.
  def __tokensFromArgs( self, * args, ** kwargs ) :
    if 's_raw' in kwargs :
      oRoot = parse.parse( self.grammar.root, s_child )
      ##! Evaluates to virtual root token.
      return oRoot.children()
    else :
      assert args
      uArg = args[ 0 ]
      if isinstance( uArg, Token ) :
        assert 1 == len( args )
        return [ uArg ]
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
        return [ oToken ]

