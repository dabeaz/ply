# lex_token2.py
#
# Tests for tokens of wrong type

import ply.lex as lex

tokens = "PLUS MINUS NUMBER"

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error(t):
    pass


lex.lex()


