# lex_token.py
#
# Regular expression rule matches empty string

import sys
sys.path.insert(0,"..")

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

import sys

lex.lex()


