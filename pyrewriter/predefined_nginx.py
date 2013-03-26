#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Predefined configuration for |nginx| config file format.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

from pyparsing import *

import pyrewriter


COMMENT = pythonStyleComment
STR = sglQuotedString | dblQuotedString
CMD = Word( alphas, alphanums + '_' )
ARG_CHARS = filter( lambda s : s not in [ ';', '{', '}' ], printables )
ARG = Word( ARG_CHARS ) | STR
EXPR = Forward()
TERM = Literal( ';' ) + Optional( COMMENT )
BLOCK_BEGIN = Literal( '{' ) + ZeroOrMore( COMMENT )
BLOCK_END = Literal( '}' ) + ZeroOrMore( COMMENT )
BLOCK = BLOCK_BEGIN + ZeroOrMore( EXPR | COMMENT ) + BLOCK_END
EXPR << CMD + ZeroOrMore( ARG | STR ) + (BLOCK | TERM )
GRAMMAR = OneOrMore( EXPR | COMMENT )

pyrewriter.capture( CMD, 'separate' )
pyrewriter.capture( ARG, 'separate' )
pyrewriter.capture( TERM, 'newline' )
pyrewriter.capture( COMMENT )
pyrewriter.capture( BLOCK_BEGIN, 'newline', 'separate' )
pyrewriter.capture( BLOCK_END, 'newline' )
pyrewriter.capture( BLOCK )
pyrewriter.capture( EXPR )

