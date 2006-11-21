#!/usr/local/bin
# ----------------------------------------------------------------------
# testyacc.py
#
# Run tests for the yacc module
# ----------------------------------------------------------------------

import sys,os,glob

if len(sys.argv) < 2:
    print "Usage: python testyacc.py directory"
    raise SystemExit

dirname = None
make = 0

for o in sys.argv[1:]:
    if o == '-make':
        make = 1
    else:
        dirname = o
        break

if not dirname:
    print "Usage: python testyacc.py [-make] directory"
    raise SystemExit

f = glob.glob("%s/%s" % (dirname,"yacc_*.py"))

print "**** Running tests for yacc ****"

for t in f:
    name = t[:-3]
    print "Testing %-32s" % name,
    os.system("rm -f %s/parsetab.*" % dirname)
    if make:
        if not os.path.exists("%s.exp" % name):
            os.system("python %s.py >%s.exp 2>&1" % (name,name))
        passed = 1
    else:
        os.system("python %s.py >%s.out 2>&1" % (name,name))
        a = os.system("diff %s.out %s.exp >%s.dif" % (name,name,name))
        if a == 0:
            passed = 1
        else:
            passed = 0

    if passed:
        print "Passed"
    else:
        print "Failed. See %s.dif" % name
        
        
                      

    
        
    
