#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# |Token| class that extends |pyparsing| parse results.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.


class Token( object ) :


  def __init__(
    self,
    ##i Token name, |None| for root token.
    s_name = None,
    ##i Text, associated with token, |None| for no text.
    s_str = None ) :

    self.__sName = s_name
    self.__lChildren = []
    self.__sStr = s_str


  @property
  def str( self ) :
    return self.__sStr


  @str.setter
  def str( self, s_str ) :
    self.__sStr = s_str


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

    def recursive( o_token, n_indent ) :
      sOut = ""
      ##  Root container token?
      if None == o_token.name :
        nIndent = n_indent
      else :
        nIndent = n_indent + 1
        if o_token.str :
          sOut += o_token.str
      for oChild in o_token.children :
        sStr = recursive( oChild, nIndent )
        if sStr :
          sOut += sStr
      return sOut

    return recursive( self, 0 )

