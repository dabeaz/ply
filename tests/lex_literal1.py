# lex_literal1.py
#
# Bad literal specification

import ply.lex as lex

tokens = [
    "NUMBER",
    ]

literals = ["+","-","**"]

def t_NUMBER(t):
    r'\d+'
    return t

def t_error(t):
    pass

lex.lex()


