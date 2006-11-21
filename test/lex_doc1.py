# lex_token.py
#
# Missing documentation string

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
def t_NUMBER(t):
    pass

def t_error(t):
    pass


import sys
sys.tracebacklimit = 0

lex.lex()


