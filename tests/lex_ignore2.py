# lex_ignore2.py
#
# ignore declaration as a raw string

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

t_ignore = r' \t'

def t_error(t):
    pass



lex.lex()


