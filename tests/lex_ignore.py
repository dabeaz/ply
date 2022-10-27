# lex_ignore.py
#
# Improperly specific ignore declaration

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_ignore(t):
    ' \t'
    pass

def t_error(t):
    pass

import sys

lex.lex()


