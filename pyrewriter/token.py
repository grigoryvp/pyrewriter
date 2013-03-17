#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# |Token| class that extends |pyparsing| parse results.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.


class Token( object ) :


  def __init__( self, s_name ) :
    self.__sName = s_name
    self.__lContent = []
    self.__sTxt = ""


  @property
  def txt( self ) :
    return self.__sTxt


  @txt.setter
  def txt( self, s_txt ) :
    self.__sTxt = s_txt


  def addChild( self, o_token ) :
    self.__lContent.append( o_token )


  def printit( self, n_indent = 0 ) :
    sIndent = ' ' * 2 * n_indent
    print( '{0}{1}({2})'.format( sIndent, self.__sName, self.__sTxt ) )
    for oItem in self.__lContent :
      oItem.printit( n_indent + 1 )

