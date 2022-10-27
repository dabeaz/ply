# lex_re2.py
#
# Regular expression rule matches empty string

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+?'
t_MINUS = r'-'
t_NUMBER = r'(\d+)'

def t_error(t):
    pass



lex.lex()


