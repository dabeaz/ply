# lex_doc1.py
#
# Missing documentation string

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

lex.lex()


