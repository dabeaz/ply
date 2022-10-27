# lex_token4.py
#
# Bad token name

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "-",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error(t):
    pass

lex.lex()


