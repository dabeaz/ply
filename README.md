# PLY - Python Lex-Yacc

Author: David Beazley (https://www.dabeaz.com)

## Introduction

PLY is a zero-dependency Python implementation of the traditional
parsing tools lex and yacc. It uses the same LALR(1) parsing algorithm
as yacc and has most of its core features. It is compatible with all
modern versions of Python.

PLY was originally created in 2001 to support an Introduction to
Compilers course at the University of Chicago.  As such, it has almost
no features other than the core LALR(1) parsing algorithm.  This is by
design--students should be made to suffer. Well, at least a little
bit.  However, from a more practical point of view, there is a lot
flexibility in terms of how you decide to use it.  You can use PLY to
build Abstract Syntax Trees (ASTs), simple one-pass compilers,
protocol decoders, or even a more advanced parsing framework.

## Important Notice - October 27, 2022

The PLY project will make no further package-installable releases.
If you want the latest version, you'll need to download it here
or clone the repo.

## Requirements

The current release of PLY requires the use of Python 3.6 or
greater. If you need to support an older version, download one of the
historical releases at https://github.com/dabeaz/archive/tree/main/ply.

## How to Install and Use 

Although PLY is open-source, it is not distributed or installed by
package manager.  There are only two files: `lex.py` and `yacc.py`,
both of which are contained in a `ply` package directory. To use PLY,
copy the `ply` directory into your project and import `lex` and `yacc`
from the associated `ply` subpackage.  Alternatively, you can install
these files into your working python using `make install`.

```python
from .ply import lex
from .ply import yacc
```

PLY has no third-party dependencies and can be freely renamed or moved
around within your project as you see fit.  It rarely changes. 

## Example

The primary use for PLY is writing parsers for programming languages. Here an
example that parses simple expressions into an abstract syntax tree (AST):

```python
# -----------------------------------------------------------------------------
# example.py
#
# Example of using PLY To parse the following simple grammar.
#
#   expression : term PLUS term
#              | term MINUS term
#              | term
#
#   term       : factor TIMES factor
#              | factor DIVIDE factor
#              | factor
#
#   factor     : NUMBER
#              | NAME
#              | PLUS factor
#              | MINUS factor
#              | LPAREN expression RPAREN
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER' )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)
```

## Documentation

The [doc/](doc/) directory has more extensive documentation on PLY.

## Examples

The [example/](example/) directory has various examples of using PLY.

## Test Suite

PLY is not shipped with a test-suite.  However, it is extensively
tested before releases are made.  The file
[ply-tests.tar.gz](https://github.com/dabeaz/ply/raw/master/ply-tests.tar.gz)
contains a current version of the tests should you want to run them on
your own.

## Bug Reports

PLY is mature software and new features are rarely added.  If you think you have
found a bug, please report an issue.

## Questions and Answers

*Q: Why does PLY have such a weird API?*

Aside from simply being over 20 years old and predating many advanced
Python features, PLY takes inspiration from two primary sources: the
Unix `yacc` utility and John Aycock's Spark toolkit. `yacc` uses a
convention of referencing grammar symbols by `$1`, `$2`, and so
forth. PLY mirrors this using `p[1]`, `p[2]`, etc.  Spark was a
parsing toolkit that utilized introspection and Python docstrings for
specifying a grammar. PLY borrowed that because it was clever.
A modern API can be found in the related [SLY](https://github.com/dabeaz/sly)
project.

*Q: Why isn't PLY distributed as a package?*

PLY is highly specialized software that is really only of interest to
people creating parsers for programming languages. In such a project,
I think you should take responsibility for library dependencies.  PLY
is very small and rarely changes--if it works for your project, there
is no reason to ever update it.  At the same time, as it's author, I
reserve the creative right to make occasional updates to the project,
including those that might introduce breaking changes.  The bottom
line is that I'm not a link in your software supply chain.  If you
use PLY, you should copy it into your project.

*Q: Do you accept pull requests and user contributions?*

No. New features are not being added to PLY at this time.  However, I
am interested in bug reports should you find a problem with PLY.  Feel
free to use the issue-tracker for feature ideas--just because PLY
is not in active development doesn't mean that good ideas will be
ignored.

*Q: Can I use PLY to make my own parsing tool?*

Absolutely! It's free software that you are free to copy and modify in
any way that makes sense. This includes remixing it into something
that's more powerful.   I'd just ask that you keep the original
copyright notice in files based on the original PLY source code so
that others know where it came from.


## Acknowledgements

A special thanks is in order for all of the students in CS326 who
suffered through about 25 different versions of this.

The CHANGES file acknowledges those who have contributed patches.

Elias Ioup did the first implementation of LALR(1) parsing in PLY-1.x. 
Andrew Waters and Markus Schoepflin were instrumental in reporting bugs
and testing a revised LALR(1) implementation for PLY-2.0.

## Take a Class!

If you'd like to learn more about compiler principles or have a go at implementing
a compiler from scratch, come take a course. https://www.dabeaz.com/compiler.html.




