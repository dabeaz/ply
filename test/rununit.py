#!/usr/bin/env python 
'''Script to run all tests using python "unittest" module''' 
 
__author__ = "Miki Tebeka <miki.tebeka@zoran.com>" 
 
from unittest import TestCase, main, makeSuite, TestSuite 
from os import popen, environ, remove 
from glob import glob 
from sys import executable, argv 
from os.path import isfile, basename, splitext 
 
# Add path to lex.py and yacc.py 
environ["PYTHONPATH"] = ".." 
 
class PLYTest(TestCase): 
    '''General test case for PLY test''' 
    def _runtest(self, filename): 
        '''Run a single test file an compare result''' 
        exp_file = filename.replace(".py", ".exp") 
        self.failUnless(isfile(exp_file), "can't find %s" % exp_file) 
        pipe = popen("%s %s 2>&1" % (executable, filename)) 
        out = pipe.read().strip() 
        self.failUnlessEqual(out, open(exp_file).read().strip()) 
 
 
class LexText(PLYTest): 
    '''Testing Lex''' 
    pass 
 
class YaccTest(PLYTest): 
    '''Testing Yacc''' 
 
    def tearDown(self): 
        '''Cleanup parsetab.py[c] file''' 
        for ext in (".py", ".pyc"): 
            fname = "parsetab%s" % ext 
            if isfile(fname): 
                remove(fname) 
 
def add_test(klass, filename): 
    '''Add a test to TestCase class''' 
    def t(self): 
        self._runtest(filename) 
    # Test name is test_FILENAME without the ./ and without the .py 
    setattr(klass, "test_%s" % (splitext(basename(filename))[0]), t) 

# Add lex tests 
for file in glob("./lex_*.py"): 
    add_test(LexText, file) 
lex_suite = makeSuite(LexText, "test_") 
 
# Add yacc tests 
for file in glob("./yacc_*.py"): 
    add_test(YaccTest, file) 
yacc_suite = makeSuite(YaccTest, "test_") 
 
# All tests suite 
test_suite = TestSuite((lex_suite, yacc_suite)) 
 
if __name__ == "__main__": 
    main() 
 
