# -----------------------------------------------------------------------------
# yacc_simple.py
#
# A simple, properly specifier grammar
# -----------------------------------------------------------------------------
import sys

if ".." not in sys.path: sys.path.insert(0,"..")
import ply.yacc as yacc
from ply.yacc import SPEC

import calclex

class CalcParser:
    tokens = calclex.tokens

    # Parsing rules
    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('right','UMINUS'),
        )

    # dictionary of names
    names = { }

    @SPEC('statement : NAME EQUALS expression')
    def p_statement_assign(self, t):
        """Assign statement"""
        names[t[1]] = t[3]

    @SPEC('statement : expression')
    def p_statement_expr(self, t):
        """Expression statement"""
        print(t[1])

    @SPEC('''expression : expression PLUS expression
                        | expression MINUS expression
                        | expression TIMES expression
                        | expression DIVIDE expression''')
    def p_expression_binop(self, t):
        """Binary operations"""
        if t[2] == '+'  : t[0] = t[1] + t[3]
        elif t[2] == '-': t[0] = t[1] - t[3]
        elif t[2] == '*': t[0] = t[1] * t[3]
        elif t[2] == '/': t[0] = t[1] / t[3]

    @SPEC('expression : MINUS expression %prec UMINUS')
    def p_expression_uminus(self, t):
        """Unary minus"""
        t[0] = -t[2]

    @SPEC('expression : LPAREN expression RPAREN')
    def p_expression_group(self, t):
        """Grouped expression"""
        t[0] = t[2]

    @SPEC('expression : NUMBER')
    def p_expression_number(self, t):
        """Number"""
        t[0] = t[1]

    @SPEC('expression : NAME')
    def p_expression_name(self, t):
        """Variable name"""
        try:
            t[0] = names[t[1]]
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)

calc = CalcParser()

# Build the parser
yacc.yacc(module=calc)




