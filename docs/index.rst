PLY (Python Lex-Yacc)
=====================

Requirements
------------

PLY requires the use of Python 3.6 or greater.  Older versions
of Python are not supported.

Overview
--------

PLY is a 100% Python implementation of the lex and yacc tools
commonly used to write parsers and compilers.  Parsing is
based on the same LALR(1) algorithm used by many yacc tools.
Here are a few notable features:

 -  PLY provides *very* extensive error reporting and diagnostic 
    information to assist in parser construction.  The original
    implementation was developed for instructional purposes.  As
    a result, the system tries to identify the most common types
    of errors made by novice users.  

 -  PLY provides full support for empty productions, error recovery,
    precedence specifiers, and moderately ambiguous grammars.

 -  PLY can be used to build parsers for "real" programming languages.
    Although it is not ultra-fast due to its Python implementation,
    PLY can be used to parse grammars consisting of several hundred
    rules (as might be found for a language like C).  

More Documentation
==================

Contents:

.. toctree::
   :maxdepth: 3

   ply
   internals

Resources
=========

For a detailed overview of parsing theory, consult the excellent
book "Compilers : Principles, Techniques, and Tools" by Aho, Sethi, and
Ullman.  The topics found in "Lex & Yacc" by Levine, Mason, and Brown
may also be useful.

The GitHub page for PLY can be found at:

     https://github.com/dabeaz/ply

Please direct bug reports and pull requests to the GitHub page.
To contact me directly, send email to dave@dabeaz.com or contact
me on Twitter (@dabeaz).

