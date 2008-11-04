# testyacc.py

import unittest
import StringIO
import sys
import os

sys.path.insert(0,"..")
sys.tracebacklimit = 0

import ply.yacc

def check_expected(result,expected):
    resultlines = result.splitlines()
    expectedlines = expected.splitlines()
    if len(resultlines) != len(expectedlines):
        return False
    for rline,eline in zip(resultlines,expectedlines):
        if not rline.endswith(eline):
            return False
    return True

def run_import(module):
    code = "import "+module
    exec code
    del sys.modules[module]
    
# Tests related to errors and warnings when building parsers
class YaccErrorWarningTests(unittest.TestCase):
    def setUp(self):
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()
        try:
            os.remove("parsetab.py")
            os.remove("parsetab.pyc")
        except OSError:
            pass
        
    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
    def test_yacc_badargs(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_badargs")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_badargs.py:23: Rule 'p_statement_assign' has too many arguments.\n"
                                    "yacc_badargs.py:27: Rule 'p_statement_expr' requires an argument.\n"
                                    ))        
    def test_yacc_badid(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_badid")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_badid.py:32: Illegal name 'bad&rule' in rule 'statement'\n"
                                    "yacc_badid.py:36: Illegal rule name 'bad&rule'\n"
                                    ))

    def test_yacc_badprec(self):
        try:
            run_import("yacc_badprec")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "precedence must be a list or tuple."))
    def test_yacc_badprec2(self):
        run_import("yacc_badprec2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Invalid precedence table.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    "yacc: 8 shift/reduce conflicts\n"
                                    ))

    def test_yacc_badprec3(self):
        run_import("yacc_badprec3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Precedence already specified for terminal 'MINUS'\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))
        
    def test_yacc_badrule(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_badrule")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_badrule.py:24: Syntax error. Expected ':'\n"
                                    "yacc_badrule.py:28: Syntax error in rule 'statement'\n"
                                    "yacc_badrule.py:33: Syntax error. Expected ':'\n"
                                    "yacc_badrule.py:42: Syntax error. Expected ':'\n"
                                    ))

    def test_yacc_badtok(self):
        try:
            run_import("yacc_badtok")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "tokens must be a list or tuple."))

    def test_yacc_dup(self):
        run_import("yacc_dup")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_dup.py:27: Function p_statement redefined. Previously defined on line 23\n"
                                    "yacc: Warning. Token 'EQUALS' defined, but not used.\n"
                                    "yacc: Warning. There is 1 unused token.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))
    def test_yacc_error1(self):
        try:
            run_import("yacc_error1")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "yacc_error1.py:61: p_error() requires 1 argument."))

    def test_yacc_error2(self):
        try:
            run_import("yacc_error2")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "yacc_error2.py:61: p_error() requires 1 argument."))

    def test_yacc_error3(self):
        try:
            run_import("yacc_error3")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "'p_error' defined, but is not a function or method."))
            
    def test_yacc_error4(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_error4")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_error4.py:62: Illegal rule name 'error'. Already defined as a token.\n"
                                    ))
        
    def test_yacc_inf(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_inf")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Warning. Token 'NUMBER' defined, but not used.\n"
                                    "yacc: Warning. There is 1 unused token.\n"
                                    "yacc: Infinite recursion detected for symbol 'statement'.\n"
                                    "yacc: Infinite recursion detected for symbol 'expression'.\n"
                                    ))
    def test_yacc_literal(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_literal")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_literal.py:36: Literal token '**' in rule 'expression' may only be a single character\n"
                                    ))
    def test_yacc_misplaced(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_misplaced")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_misplaced.py:32: Misplaced '|'.\n"
                                    ))

    def test_yacc_missing1(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_missing1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_missing1.py:24: Symbol 'location' used, but not defined as a token or a rule.\n"
                                    ))

    def test_yacc_nested(self):
        run_import("yacc_nested")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "A\n"
                                    "A\n"
                                    "A\n",
                                    ))

    def test_yacc_nodoc(self):
        run_import("yacc_nodoc")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_nodoc.py:27: No documentation string specified in function 'p_statement_expr'\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))

    def test_yacc_noerror(self):
        run_import("yacc_noerror")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Warning. no p_error() function is defined.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))

    def test_yacc_nop(self):
        run_import("yacc_nop")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_nop.py:27: Warning. Possible grammar rule 'statement_expr' defined without p_ prefix.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))

    def test_yacc_notfunc(self):
        run_import("yacc_notfunc")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Warning. 'p_statement_assign' not defined as a function\n"
                                    "yacc: Warning. Token 'EQUALS' defined, but not used.\n"
                                    "yacc: Warning. There is 1 unused token.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))
    def test_yacc_notok(self):
        try:
            run_import("yacc_notok")
        except ply.yacc.YaccError,e:
            self.assert_(check_expected(str(e),
                                        "module does not define a list 'tokens'"))

    def test_yacc_rr(self):
        run_import("yacc_rr")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Generating LALR parsing table...\n"
                                    "yacc: 1 reduce/reduce conflict\n"
                                    ))
    def test_yacc_simple(self):
        run_import("yacc_simple")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Generating LALR parsing table...\n"
                                    ))
    def test_yacc_sr(self):
        run_import("yacc_sr")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Generating LALR parsing table...\n"
                                    "yacc: 20 shift/reduce conflicts\n"
                                    ))

    def test_yacc_term1(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_term1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_term1.py:24: Illegal rule name 'NUMBER'. Already defined as a token.\n"
                                    ))

    def test_yacc_unused(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_unused")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_unused.py:62: Symbol 'COMMA' used, but not defined as a token or a rule.\n"
                                    "yacc: Symbol 'COMMA' is unreachable.\n"
                                    "yacc: Symbol 'exprlist' is unreachable.\n"
                                    ))
    def test_yacc_unused_rule(self):
        run_import("yacc_unused_rule")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_unused_rule.py:62: Warning. Rule 'integer' defined, but not used.\n"
                                    "yacc: Warning. There is 1 unused rule.\n"
                                    "yacc: Symbol 'integer' is unreachable.\n"
                                    "yacc: Generating LALR parsing table...\n"
                                    ))

    def test_yacc_uprec(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_uprec")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_uprec.py:37: Nothing known about the precedence of 'UMINUS'\n"
                                    ))

    def test_yacc_uprec2(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_uprec2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc_uprec2.py:37: Syntax error. Nothing follows %prec.\n"
                                    ))

    def test_yacc_prec1(self):
        self.assertRaises(ply.yacc.YaccError,run_import,"yacc_prec1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "yacc: Precedence rule 'left' defined for unknown symbol '+'\n"
                                    "yacc: Precedence rule 'left' defined for unknown symbol '*'\n"
                                    "yacc: Precedence rule 'left' defined for unknown symbol '-'\n"
                                    "yacc: Precedence rule 'left' defined for unknown symbol '/'\n"
                                    ))


            
unittest.main()
