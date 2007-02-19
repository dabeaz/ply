# lex_token.py
#
# ignore declaration as a raw string

import sys
sys.path.insert(0,"..")

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

t_ignore = r' \t'

def t_error(t):
    pass

import sys

lex.lex()


