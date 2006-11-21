# lex_token.py
#
# t_error defined, but not function

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

t_error = "foo"

sys.tracebacklimit = 0

lex.lex()


