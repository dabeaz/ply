# lex_token1.py
#
# Tests for absence of tokens variable

import ply.lex as lex

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error(t):
    pass

lex.lex()


