# lex_token.py
#
# Rule defined as some other type

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
t_NUMBER = 1

def t_error(t):
    pass

sys.tracebacklimit = 0

lex.lex()


