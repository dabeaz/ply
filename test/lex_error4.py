# lex_token.py
#
# t_error defined as function, but too many args

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

def t_error(t,s):
    pass

sys.tracebacklimit = 0

lex.lex()


