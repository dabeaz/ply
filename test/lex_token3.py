# lex_token.py
#
# tokens is right type, but is missing a token for one rule

import sys
sys.path.insert(0,"..")

import ply.lex as lex

tokens = [
    "PLUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error(t):
    pass


sys.tracebacklimit = 0

lex.lex()


