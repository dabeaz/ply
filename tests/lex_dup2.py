# lex_dup2.py
#
# Duplicated rule specifiers

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
def t_NUMBER(t):
    r'\d+'
    pass

def t_NUMBER(t):
    r'\d+'
    pass

def t_error(t):
    pass



lex.lex()


