# testlex.py

import unittest
import StringIO
import sys
sys.path.insert(0,"..")
sys.tracebacklimit = 0

import ply.lex

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
    
# Tests related to errors and warnings when building lexers
class LexErrorWarningTests(unittest.TestCase):
    def setUp(self):
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()
    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
    def test_lex_doc1(self):
        run_import("lex_doc1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                              "lex_doc1.py:18: No regular expression defined for rule 't_NUMBER'\n"))
    def test_lex_dup1(self):
        self.assertRaises(SyntaxError,run_import,"lex_dup1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_dup1.py:20: Rule t_NUMBER redefined. Previously defined on line 18\n" ))        
        
    def test_lex_dup2(self):
        self.assertRaises(SyntaxError,run_import,"lex_dup2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_dup2.py:22: Rule t_NUMBER redefined. Previously defined on line 18\n" ))
            
    def test_lex_dup3(self):
        self.assertRaises(SyntaxError,run_import,"lex_dup3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_dup3.py:20: Rule t_NUMBER redefined. Previously defined on line 18\n" ))

    def test_lex_empty(self):
        try:
            run_import("lex_empty")
        except SyntaxError,e:
            pass
        self.assertEquals(str(e),"lex: no rules of the form t_rulename are defined.")

    def test_lex_error1(self):
        run_import("lex_error1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Warning. no t_error rule is defined.\n"))

    def test_lex_error2(self):
        try:
            run_import("lex_error2")
        except SyntaxError,e:
            pass
        self.assertEquals(str(e),"lex: Rule 't_error' must be defined as a function")

    def test_lex_error3(self):
        self.assertRaises(SyntaxError,run_import,"lex_error3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_error3.py:20: Rule 't_error' requires an argument.\n"))

    def test_lex_error4(self):
        self.assertRaises(SyntaxError,run_import,"lex_error4")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_error4.py:20: Rule 't_error' has too many arguments.\n"))

    def test_lex_ignore(self):
        self.assertRaises(SyntaxError,run_import,"lex_ignore")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_ignore.py:20: Rule 't_ignore' must be defined as a string.\n"))

    def test_lex_ignore2(self):
        run_import("lex_ignore2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Warning. t_ignore contains a literal backslash '\\'\n"))

    def test_lex_nowarn(self):
        run_import("lex_nowarn")
        self.assertEquals(sys.stderr.getvalue(),"")
        self.assertEquals(sys.stdout.getvalue(),"")

    def test_lex_re1(self):
        self.assertRaises(SyntaxError,run_import,"lex_re1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Invalid regular expression for rule 't_NUMBER'. unbalanced parenthesis\n"))

    def test_lex_re2(self):
        self.assertRaises(SyntaxError,run_import,"lex_re2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Regular expression for rule 't_PLUS' matches empty string.\n"))

    def test_lex_re3(self):
        self.assertRaises(SyntaxError,run_import,"lex_re3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Invalid regular expression for rule 't_POUND'. unbalanced parenthesis\n"
                                    "lex: Make sure '#' in rule 't_POUND' is escaped with '\\#'.\n"))

    def test_lex_rule1(self):
        self.assertRaises(SyntaxError,run_import,"lex_rule1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: t_NUMBER not defined as a function or string\n"))

    def test_lex_rule2(self):
        self.assertRaises(SyntaxError,run_import,"lex_rule2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_rule2.py:18: Rule 't_NUMBER' requires an argument.\n"))

    def test_lex_rule3(self):
        self.assertRaises(SyntaxError,run_import,"lex_rule3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex_rule3.py:18: Rule 't_NUMBER' has too many arguments.\n"))


    def test_lex_state1(self):
        self.assertRaises(SyntaxError,run_import,"lex_state1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: states must be defined as a tuple or list.\n"))

    def test_lex_state2(self):
        self.assertRaises(SyntaxError,run_import,"lex_state2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: invalid state specifier 'comment'. Must be a tuple (statename,'exclusive|inclusive')\n"
                                    "lex: invalid state specifier 'example'. Must be a tuple (statename,'exclusive|inclusive')\n"))

    def test_lex_state3(self):
        self.assertRaises(SyntaxError,run_import,"lex_state3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: state name 1 must be a string\n"
                                    "lex: No rules defined for state 'example'\n"))

    def test_lex_state4(self):
        self.assertRaises(SyntaxError,run_import,"lex_state4")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: state type for state comment must be 'inclusive' or 'exclusive'\n"))


    def test_lex_state5(self):
        self.assertRaises(SyntaxError,run_import,"lex_state5")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: state 'comment' already defined.\n"))

    def test_lex_state_noerror(self):
        run_import("lex_state_noerror")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Warning. no error rule is defined for exclusive state 'comment'\n"))    

    def test_lex_state_norule(self):
        self.assertRaises(SyntaxError,run_import,"lex_state_norule")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: No rules defined for state 'example'\n"))

    def test_lex_token1(self):
        try:
            run_import("lex_token1")
        except SyntaxError,e:
            pass
        self.assertEquals(str(e),"lex: module does not define 'tokens'")


    def test_lex_token2(self):
        try:
            run_import("lex_token2")
        except SyntaxError,e:
            pass
        self.assertEquals(str(e),"lex: tokens must be a list or tuple.")

    
    def test_lex_token3(self):
        self.assertRaises(SyntaxError,run_import,"lex_token3")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Rule 't_MINUS' defined for an unspecified token MINUS.\n"))


    def test_lex_token4(self):
        self.assertRaises(SyntaxError,run_import,"lex_token4")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Bad token name '-'\n"))


    def test_lex_token5(self):
        try:
            run_import("lex_token5")
        except ply.lex.LexError,e:
            pass
        self.assert_(check_expected(str(e),"lex_token5.py:19: Rule 't_NUMBER' returned an unknown token type 'NUM'"))

    def test_lex_token_dup(self):
        run_import("lex_token_dup")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Warning. Token 'MINUS' multiply defined.\n"))   

        
    def test_lex_literal1(self):
        self.assertRaises(SyntaxError,run_import,"lex_literal1")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Invalid literal '**'. Must be a single character\n"))

    def test_lex_literal2(self):
        self.assertRaises(SyntaxError,run_import,"lex_literal2")
        result = sys.stderr.getvalue()
        self.assert_(check_expected(result,
                                    "lex: Invalid literals specification. literals must be a sequence of characters.\n"))

import os
import subprocess
import shutil

# Tests related to various build options associated with lexers
class LexBuildOptionTests(unittest.TestCase):
    def setUp(self):
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()
    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        try:
            shutil.rmtree("lexdir")
        except OSError:
            pass

    def test_lex_module(self):
        run_import("lex_module")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        
    def test_lex_object(self):
        run_import("lex_object")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))

    def test_lex_closure(self):
        run_import("lex_closure")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
    def test_lex_optimize(self):
        try:
            os.remove("lextab.py")
        except OSError:
            pass
        try:
            os.remove("lextab.pyc")
        except OSError:
            pass
        try:
            os.remove("lextab.pyo")
        except OSError:
            pass
        run_import("lex_optimize")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lextab.py"))

        p = subprocess.Popen(['python','-O','lex_optimize.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lextab.pyo"))
        os.remove("lextab.pyo")
        p = subprocess.Popen(['python','-OO','lex_optimize.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lextab.pyo"))
        try:
            os.remove("lextab.py")
        except OSError:
            pass
        try:
            os.remove("lextab.pyc")
        except OSError:
            pass
        try:
            os.remove("lextab.pyo")
        except OSError:
            pass

    def test_lex_optimize2(self):
        try:
            os.remove("opt2tab.py")
        except OSError:
            pass
        try:
            os.remove("opt2tab.pyc")
        except OSError:
            pass
        try:
            os.remove("opt2tab.pyo")
        except OSError:
            pass
        run_import("lex_optimize2")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("opt2tab.py"))

        p = subprocess.Popen(['python','-O','lex_optimize2.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("opt2tab.pyo"))
        os.remove("opt2tab.pyo")
        p = subprocess.Popen(['python','-OO','lex_optimize2.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("opt2tab.pyo"))
        try:
            os.remove("opt2tab.py")
        except OSError:
            pass
        try:
            os.remove("opt2tab.pyc")
        except OSError:
            pass
        try:
            os.remove("opt2tab.pyo")
        except OSError:
            pass

    def test_lex_optimize3(self):
        try:
            shutil.rmtree("lexdir")
        except OSError:
            pass
        
        os.mkdir("lexdir")
        os.mkdir("lexdir/sub")
        open("lexdir/__init__.py","w").write("")
        open("lexdir/sub/__init__.py","w").write("")
        run_import("lex_optimize3")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lexdir/sub/calctab.py"))

        p = subprocess.Popen(['python','-O','lex_optimize3.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lexdir/sub/calctab.pyo"))
        os.remove("lexdir/sub/calctab.pyo")
        p = subprocess.Popen(['python','-OO','lex_optimize3.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(PLUS,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("lexdir/sub/calctab.pyo"))
        try:
            shutil.rmtree("lexdir")
        except OSError:
            pass

    def test_lex_opt_alias(self):
        try:
            os.remove("aliastab.py")
        except OSError:
            pass
        try:
            os.remove("aliastab.pyc")
        except OSError:
            pass
        try:
            os.remove("aliastab.pyo")
        except OSError:
            pass
        run_import("lex_opt_alias")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(+,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("aliastab.py"))

        p = subprocess.Popen(['python','-O','lex_opt_alias.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(+,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("aliastab.pyo"))
        os.remove("aliastab.pyo")
        p = subprocess.Popen(['python','-OO','lex_opt_alias.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(NUMBER,3,1,0)\n"
                                    "(+,'+',1,1)\n"
                                    "(NUMBER,4,1,2)\n"))
        self.assert_(os.path.exists("aliastab.pyo"))
        try:
            os.remove("aliastab.py")
        except OSError:
            pass
        try:
            os.remove("aliastab.pyc")
        except OSError:
            pass
        try:
            os.remove("aliastab.pyo")
        except OSError:
            pass

    def test_lex_many_tokens(self):
        try:
            os.remove("manytab.py")
        except OSError:
            pass
        try:
            os.remove("manytab.pyc")
        except OSError:
            pass
        try:
            os.remove("manytab.pyo")
        except OSError:
            pass
        run_import("lex_many_tokens")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(TOK34,'TOK34:',1,0)\n"
                                    "(TOK143,'TOK143:',1,7)\n"
                                    "(TOK269,'TOK269:',1,15)\n"
                                    "(TOK372,'TOK372:',1,23)\n"
                                    "(TOK452,'TOK452:',1,31)\n"
                                    "(TOK561,'TOK561:',1,39)\n"
                                    "(TOK999,'TOK999:',1,47)\n"
                                    ))

        self.assert_(os.path.exists("manytab.py"))

        p = subprocess.Popen(['python','-O','lex_many_tokens.py'],
                             stdout=subprocess.PIPE)
        result = p.stdout.read()
        self.assert_(check_expected(result,
                                    "(TOK34,'TOK34:',1,0)\n"
                                    "(TOK143,'TOK143:',1,7)\n"
                                    "(TOK269,'TOK269:',1,15)\n"
                                    "(TOK372,'TOK372:',1,23)\n"
                                    "(TOK452,'TOK452:',1,31)\n"
                                    "(TOK561,'TOK561:',1,39)\n"
                                    "(TOK999,'TOK999:',1,47)\n"
                                    ))

        self.assert_(os.path.exists("manytab.pyo"))
        os.remove("manytab.pyo")
        try:
            os.remove("manytab.py")
        except OSError:
            pass
        try:
            os.remove("manytab.pyc")
        except OSError:
            pass
        try:
            os.remove("manytab.pyo")
        except OSError:
            pass
        
# Tests related to run-time behavior of lexers
class LexRunTests(unittest.TestCase):
    def setUp(self):
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()
    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

    def test_lex_hedit(self):
        run_import("lex_hedit")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(H_EDIT_DESCRIPTOR,'abc',1,0)\n"
                                    "(H_EDIT_DESCRIPTOR,'abcdefghij',1,6)\n"
                                    "(H_EDIT_DESCRIPTOR,'xy',1,20)\n"))
       
    def test_lex_state_try(self):
        run_import("lex_state_try")
        result = sys.stdout.getvalue()
        self.assert_(check_expected(result,
                                    "(NUMBER,'3',1,0)\n"
                                    "(PLUS,'+',1,2)\n"
                                    "(NUMBER,'4',1,4)\n"
                                    "Entering comment state\n"
                                    "comment body LexToken(body_part,'This is a comment */',1,9)\n"
                                    "(PLUS,'+',1,30)\n"
                                    "(NUMBER,'10',1,32)\n"
                                    ))    



unittest.main()
