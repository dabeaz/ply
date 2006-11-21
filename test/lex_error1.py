# lex_token.py
#
# Missing t_error() rule

import sys
sys.path.insert(0,"..")

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

sys.tracebacklimit = 0

lex.lex()


