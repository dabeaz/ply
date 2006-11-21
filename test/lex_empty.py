# lex_token.py
#
# No rules defined

import sys
sys.path.insert(0,"..")

import ply.lex as lex

tokens = [
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

sys.tracebacklimit = 0

lex.lex()


