#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Predefined configuration for |nginx| config file format.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

from pyparsing import *

import pyrewriter


CMD = Word( alphas, alphanums + '_' )
STR = sglQuotedString | dblQuotedString
ARG_CHARS = filter( lambda s : s not in [ ';', '{', '}' ], printables )
ARG = Word( ARG_CHARS ) | STR
EXPR = Forward()
TERM = Literal( ';' )
COMMENT = pythonStyleComment
BLOCK_BEGIN = Literal( '{' ) + ZeroOrMore( COMMENT )
BLOCK_END = Literal( '}' ) + ZeroOrMore( COMMENT )
BLOCK = BLOCK_BEGIN + ZeroOrMore( EXPR | COMMENT ) + BLOCK_END
EXPR << CMD + ZeroOrMore( ARG | STR ) + (BLOCK | COMMENT | TERM)
GRAMMAR = OneOrMore( EXPR | COMMENT )

pyrewriter.capture( CMD )
pyrewriter.capture( ARG )
pyrewriter.capture( TERM )
pyrewriter.capture( COMMENT )
pyrewriter.capture( BLOCK_BEGIN )
pyrewriter.capture( BLOCK_END )
pyrewriter.capture( BLOCK )
pyrewriter.capture( EXPR )

