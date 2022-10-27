# lex_error3.py
#
# t_error defined as function, but with wrong # args

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error():
    pass



lex.lex()


