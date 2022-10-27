# lex_error4.py
#
# t_error defined as function, but too many args

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



lex.lex()


