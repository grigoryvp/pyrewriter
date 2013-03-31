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


  ##@ Modification API.


  ##x Add specified token as sibling before this token.
  ##  Token can be specified following ways:
  ##  * As |Token| object.
  ##  * As |Token.name| string.
  ##  * As |Token.name| and |Token.val| strings.
  ##  * As |s_raw| string that will be parsed via token grammar.
  def addSiblingBefore( self, * args, ** kwargs ) :
    return self.__addSibling( f_after = False, * args, ** kwargs )


  ##x Add specified token as sibling after this token.
  ##  Token can be specified following ways:
  ##  * As |Token| object.
  ##  * As |Token.name| string.
  ##  * As |Token.name| and |Token.val| strings.
  ##  * As |s_raw| string that will be parsed via token grammar.
  def addSiblingAfter( self, * args, ** kwargs ) :
    return self.__addSibling( f_after = True, * args, ** kwargs )


  ##x Add specified token as direct child of this token.
  ##  Token can be specified following ways:
  ##  * As |Token| object.
  ##  * As |Token.name| string.
  ##  * As |Token.name| and |Token.val| strings.
  ##  * As |s_raw| string that will be parsed via token grammar.
  def addChild( self, * args, ** kwargs ) :
    for oToken in self.__tokensFromArgs( * args, ** kwargs ) :
      oToken.parent = self
      self.__lChildren.append( oToken )
    return oToken


  ##x Replace this token with specified token.
  ##  Token can be specified following ways:
  ##  * As |Token| object.
  ##  * As |Token.name| string.
  ##  * As |Token.name| and |Token.val| strings.
  ##  * As |s_raw| string that will be parsed via token grammar.
  ##! If token is specified as raw string and parsing evaluates to more
  ##  that one token, all of them will be added.
  def replace( self, * args, ** kwargs ) :
    assert self.parent
    oReplaced = self.addSiblingAfter( * args, ** kwargs )
    self.parent.__lChildren.remove( self )
    return oReplaced


  ##@ Search API.


  def sibling( self, s_name, s_val = None ) :
    lSiblings = self.siblings( s_name, s_val )
    if lSiblings :
      self.found = lSiblings[ 0 ]
    else :
      self.found = None
    return self.found


  def siblings( self, s_name, s_val = None ) :
    if self.parent :
      return self.parent.__descendants( s_name, s_val, f_recursive = False )
    return ListEx()


  def child( self, s_name = None, s_val = None ) :
    lChildren = self.children( s_name, s_val )
    if lChildren :
      self.found = lChildren[ 0 ]
    else :
      self.found = None
    return self.found


  def children( self, s_name = None, s_val = None ) :
    if not s_name :
      return ListEx( self.__lChildren )
    return self.__descendants( s_name, s_val, f_recursive = False )


  def descendant( self, s_name, s_val = None ) :
    lDescendants = self.descendants( s_name, s_val )
    if lDescendants :
      self.found = lDescendants[ 0 ]
    else :
      self.found = None
    return self.found


  def descendants( self, s_name, s_val = None ) :
    return self.__descendants( s_name, s_val, f_recursive = True )


  ##x XPath-like search.
  def search( s_query ) :
    ##  Current search direction, '/' for child, ',' for sibling.
    sDirection = None
    for sRule in self.__splitex( s_query, '/,' ) :
      if sRule in '/,' :
        sDirection = sRule
      else :
        if not sRule :
          raise "direction is not followed by condition"
        if not sDirection :
          raise "condition is not preceded by direction"
        if sRule.startswith( '(' ) and sRule.endswith( ')' ) :
          sRule = sRule[ 1 : -1 ]
          fCapture = True
        else :
          fCapture = False
        sName, _, sVal = sRule.partition( '=' )
        if '/' == sDirection :
          for oToken in self.children( sName, sVal ) :
            pass
            # recursive( oToken )
        if ',' == sDirection :
          for oToken in self.siblings( sName, sVal ) :
            pass
            # recursive( oToken )


  ##@ Output API.


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


  ##@ Implementation.


  ##x Used by |addChild|, |addSibling| etc. Creates token from args that
  ##  can be token, one string for name, string and other value for name
  ##  and val, |s_raw| keywoard arg for raw text token representation that
  ##  need to be parsed.
  def __tokensFromArgs( self, * args, ** kwargs ) :
    if 's_raw' in kwargs :
      oRoot = parse.parse( self.grammar.root, kwargs[ 's_raw' ] )
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


  def __addSibling( self, f_after, * args, ** kwargs ) :
    assert self.parent
    for nChild, oChild in enumerate( self.parent.__lChildren ) :
      if oChild == self :
        lTokens = self.__tokensFromArgs( * args, ** kwargs )
        for nToken, oToken in enumerate( lTokens ) :
          oToken.parent = self.parent
          nInsertPos = nChild + nToken
          if f_after :
            nInsertPos += 1
          self.parent.__lChildren.insert( nInsertPos, oToken )
        break
    else :
      assert False, "internal consistency error"
    return oToken


  ##x Splits specified text using delimiter characters from specified
  ##  delimiters string. Evaluates to list of parts and delimiters.
  def __splitex( s_txt, s_delimiters ) :
    sAccum = ""
    lResult = []
    for s in s_txt :
      if s in s_delimiters :
        lResult.append( sAccum )
        sAccum = ""
      else :
        sAccum += s
    return lResult

