try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "ply",
            description="Python Lex & Yacc",
            long_description = """
PLY is yet another implementation of lex and yacc for Python. Although several other
parsing tools are available for Python, there are several reasons why you might
want to take a look at PLY: 

It's implemented entirely in Python. 

It uses LR-parsing which is reasonably efficient and well suited for larger grammars. 

PLY provides most of the standard lex/yacc features including support for empty 
productions, precedence rules, error recovery, and support for ambiguous grammars. 

PLY is extremely easy to use and provides very extensive error checking. 
""",
            license="""Lesser GPL (LGPL)""",
            version = "3.0",
            author = "David Beazley",
            author_email = "dave@dabeaz.com",
            maintainer = "David Beazley",
            maintainer_email = "dave@dabeaz.com",
            url = "http://www.dabeaz.com/ply/",
            packages = ['ply'],
            )
