# lex_re3.py
#
# Regular expression rule matches empty string

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    "POUND",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'(\d+)'
t_POUND = r'#'

def t_error(t):
    pass



lex.lex()


