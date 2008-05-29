# lex_nowarn.py
#
# Missing t_error() rule

import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    "NUMBER",
    ]

states = (('foo','exclusive'),)

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

t_foo_NUMBER = r'\d+'



lex.lex(nowarn=1)


