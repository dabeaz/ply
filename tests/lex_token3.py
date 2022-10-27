# lex_token3.py
#
# tokens is right type, but is missing a token for one rule

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

lex.lex()


