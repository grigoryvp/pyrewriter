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
    s_txt = None ) :

    self.__sName = s_name
    self.__lContent = []
    self.__sTxt = None


  @property
  def txt( self ) :
    return self.__sTxt


  @txt.setter
  def txt( self, s_txt ) :
    self.__sTxt = s_txt


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
      sTxt = None
      if 2 == len( args ) :
        uArg = args[ 1 ]
        assert isinstance( uArg, basestring )
        sTxt = uArg
      oToken = Token( sName, sTxt )
    self.__lContent.append( oToken )
    return oToken


  def printit( self, n_indent = 0 ) :
    sIndent = ' ' * 2 * n_indent
    print( '{0}{1}({2})'.format( sIndent, self.__sName, self.__sTxt ) )
    for oItem in self.__lContent :
      oItem.printit( n_indent + 1 )

