PLY Internals
=============

1. Introduction
---------------

This document describes classes and functions that make up the internal
operation of PLY.  Using this programming interface, it is possible to
manually build an parser using a different interface specification
than what PLY normally uses.  For example, you could build a gramar
from information parsed in a completely different input format.  Some of
these objects may be useful for building more advanced parsing engines
such as GLR.

It should be stressed that using PLY at this level is not for the
faint of heart.  Generally, it's assumed that you know a bit of
the underlying compiler theory and how an LR parser is put together.

2. Grammar Class
----------------

The file ``ply.yacc`` defines a class ``Grammar`` that 
is used to hold and manipulate information about a grammar
specification.   It encapsulates the same basic information
about a grammar that is put into a YACC file including 
the list of tokens, precedence rules, and grammar rules. 
Various operations are provided to perform different validations
on the grammar.  In addition, there are operations to compute
the first and follow sets that are needed by the various table
generation algorithms.


``Grammar(terminals)``
    Creates a new grammar object.  ``terminals`` is a list of strings
    specifying the terminals for the grammar.  An instance ``g`` of
    ``Grammar`` has the following methods:


``g.set_precedence(term,assoc,level)``
    Sets the precedence level and associativity for a given terminal ``term``.  
    ``assoc`` is one of ``'right'``,
    ``'left'``, or ``'nonassoc'`` and ``level`` is a positive integer.  The higher
    the value of ``level``, the higher the precedence.  Here is an example of typical
    precedence settings::
    
        g.set_precedence('PLUS',  'left',1)
        g.set_precedence('MINUS', 'left',1)
        g.set_precedence('TIMES', 'left',2)
        g.set_precedence('DIVIDE','left',2)
        g.set_precedence('UMINUS','left',3)
    
    This method must be called prior to adding any productions to the
    grammar with ``g.add_production()``.  The precedence of individual grammar
    rules is determined by the precedence of the right-most terminal.
    

``g.add_production(name,syms,func=None,file='',line=0)``
    Adds a new grammar rule.  ``name`` is the name of the rule,
    ``syms`` is a list of symbols making up the right hand
    side of the rule, ``func`` is the function to call when
    reducing the rule.   ``file`` and ``line`` specify
    the filename and line number of the rule and are used for
    generating error messages.    
    
    The list of symbols in ``syms`` may include character
    literals and ``%prec`` specifiers.  Here are some
    examples::
    
        g.add_production('expr',['expr','PLUS','term'],func,file,line)
        g.add_production('expr',['expr','"+"','term'],func,file,line)
        g.add_production('expr',['MINUS','expr','%prec','UMINUS'],func,file,line)
    
    If any kind of error is detected, a ``GrammarError`` exception
    is raised with a message indicating the reason for the failure.


``g.set_start(start=None)``
    Sets the starting rule for the grammar.  ``start`` is a string
    specifying the name of the start rule.   If ``start`` is omitted,
    the first grammar rule added with ``add_production()`` is taken to be
    the starting rule.  This method must always be called after all
    productions have been added.

``g.find_unreachable()``
    Diagnostic function.  Returns a list of all unreachable non-terminals
    defined in the grammar.  This is used to identify inactive parts of
    the grammar specification.

``g.infinite_cycle()``
    Diagnostic function.  Returns a list of all non-terminals in the
    grammar that result in an infinite cycle.  This condition occurs if
    there is no way for a grammar rule to expand to a string containing
    only terminal symbols.

``g.undefined_symbols()``
    Diagnostic function.  Returns a list of tuples ``(name, prod)``
    corresponding to undefined symbols in the grammar. ``name`` is the
    name of the undefined symbol and ``prod`` is an instance of 
    ``Production`` which has information about the production rule
    where the undefined symbol was used.

``g.unused_terminals()``
    Diagnostic function.  Returns a list of terminals that were defined,
    but never used in the grammar.

``g.unused_rules()``
    Diagnostic function.  Returns a list of ``Production`` instances
    corresponding to production rules that were defined in the grammar,
    but never used anywhere.  This is slightly different
    than ``find_unreachable()``.

``g.unused_precedence()``
    Diagnostic function.  Returns a list of tuples ``(term, assoc)`` 
    corresponding to precedence rules that were set, but never used the
    grammar.  ``term`` is the terminal name and ``assoc`` is the
    precedence associativity (e.g., ``'left'``, ``'right'``, 
    or ``'nonassoc'``.

``g.compute_first()``
    Compute all of the first sets for all symbols in the grammar.  Returns a dictionary
    mapping symbol names to a list of all first symbols.

``g.compute_follow()``
    Compute all of the follow sets for all non-terminals in the grammar.
    The follow set is the set of all possible symbols that might follow a
    given non-terminal.  Returns a dictionary mapping non-terminal names
    to a list of symbols.

``g.build_lritems()``
    Calculates all of the LR items for all productions in the grammar.  This
    step is required before using the grammar for any kind of table generation.
    See the section on LR items below.

The following attributes are set by the above methods and may be useful
in code that works with the grammar.  All of these attributes should be
assumed to be read-only.  Changing their values directly will likely 
break the grammar.

``g.Productions``
    A list of all productions added.  The first entry is reserved for
    a production representing the starting rule.  The objects in this list
    are instances of the ``Production`` class, described shortly.

``g.Prodnames``
    A dictionary mapping the names of nonterminals to a list of all
    productions of that nonterminal.

``g.Terminals``
    A dictionary mapping the names of terminals to a list of the
    production numbers where they are used.

``g.Nonterminals``
    A dictionary mapping the names of nonterminals to a list of the
    production numbers where they are used.

``g.First``
    A dictionary representing the first sets for all grammar symbols.  This is
    computed and returned by the ``compute_first()`` method.

``g.Follow``
    A dictionary representing the follow sets for all grammar rules.  This is
    computed and returned by the ``compute_follow()`` method.

``g.Start``
    Starting symbol for the grammar.  Set by the ``set_start()`` method.

For the purposes of debugging, a ``Grammar`` object supports the ``__len__()`` and
``__getitem__()`` special methods.  Accessing ``g[n]`` returns the nth production
from the grammar.

3. Productions
--------------

``Grammar`` objects store grammar rules as instances of a ``Production`` class.  This
class has no public constructor--you should only create productions by calling ``Grammar.add_production()``.
The following attributes are available on a ``Production`` instance ``p``.

``p.name``
    The name of the production. For a grammar rule such as ``A : B C D``, this is ``'A'``.

``p.prod``
    A tuple of symbols making up the right-hand side of the production.  For a grammar rule such as ``A : B C D``, this is ``('B','C','D')``.

``p.number``
    Production number.  An integer containing the index of the production in the grammar's ``Productions`` list.

``p.func``
    The name of the reduction function associated with the production.
    This is the function that will execute when reducing the entire
    grammar rule during parsing.

``p.callable``
    The callable object associated with the name in ``p.func``.  This is ``None``
    unless the production has been bound using ``bind()``.

``p.file``
    Filename associated with the production.  Typically this is the file where the production was defined.  Used for error messages.

``p.lineno``
    Line number associated with the production.  Typically this is the line number in ``p.file`` where the production was defined.  Used for error messages.

``p.prec``
    Precedence and associativity associated with the production.  This is a tuple ``(assoc,level)`` where
    ``assoc`` is one of ``'left'``,``'right'``, or ``'nonassoc'`` and ``level`` is
    an integer.   This value is determined by the precedence of the right-most terminal symbol in the production
    or by use of the ``%prec`` specifier when adding the production.

``p.usyms``
    A list of all unique symbols found in the production.

``p.lr_items``
    A list of all LR items for this production.  This attribute only has a meaningful value if the
    ``Grammar.build_lritems()`` method has been called.  The items in this list are 
    instances of ``LRItem`` described below.

``p.lr_next``
    The head of a linked-list representation of the LR items in ``p.lr_items``.  
    This attribute only has a meaningful value if the ``Grammar.build_lritems()`` 
    method has been called.  Each ``LRItem`` instance has a ``lr_next`` attribute
    to move to the next item.  The list is terminated by ``None``.

``p.bind(dict)``
    Binds the production function name in ``p.func`` to a callable object in 
    ``dict``.   This operation is typically carried out in the last step
    prior to running the parsing engine and is needed since parsing tables are typically
    read from files which only include the function names, not the functions themselves.

``Production`` objects support
the ``__len__()``, ``__getitem__()``, and ``__str__()``
special methods.
``len(p)`` returns the number of symbols in ``p.prod``
and ``p[n]`` is the same as ``p.prod[n]``. 

4. LRItems
----------

The construction of parsing tables in an LR-based parser generator is primarily
done over a set of "LR Items".   An LR item represents a stage of parsing one
of the grammar rules.   To compute the LR items, it is first necessary to
call ``Grammar.build_lritems()``.  Once this step, all of the productions
in the grammar will have their LR items attached to them.

Here is an interactive example that shows what LR items look like if you
interactively experiment.  In this example, ``g`` is a ``Grammar`` 
object::

    >>> g.build_lritems()
    >>> p = g[1]
    >>> p
    Production(statement -> ID = expr)
    >>>

In the above code, ``p`` represents the first grammar rule. In
this case, a rule ``'statement -> ID = expr'``.

Now, let's look at the LR items for ``p``::

    >>> p.lr_items
    [LRItem(statement -> . ID = expr), 
     LRItem(statement -> ID . = expr), 
     LRItem(statement -> ID = . expr), 
     LRItem(statement -> ID = expr .)]
    >>>

In each LR item, the dot (.) represents a specific stage of parsing.  In each LR item, the dot
is advanced by one symbol.  It is only when the dot reaches the very end that a production
is successfully parsed.

An instance ``lr`` of ``LRItem`` has the following
attributes that hold information related to that specific stage of
parsing.

``lr.name``
    The name of the grammar rule. For example, ``'statement'`` in the above example.

``lr.prod``
    A tuple of symbols representing the right-hand side of the production, including the
    special ``'.'`` character.  For example, ``('ID','.','=','expr')``.

``lr.number``
    An integer representing the production number in the grammar.

``lr.usyms``
    A set of unique symbols in the production.  Inherited from the original ``Production`` instance.

``lr.lr_index``
    An integer representing the position of the dot (.).  You should never use ``lr.prod.index()``
    to search for it--the result will be wrong if the grammar happens to also use (.) as a character
    literal.

``lr.lr_after``
    A list of all productions that can legally appear immediately to the right of the
    dot (.).  This list contains ``Production`` instances.   This attribute
    represents all of the possible branches a parse can take from the current position.
    For example, suppose that ``lr`` represents a stage immediately before
    an expression like this::
    
        >>> lr
        LRItem(statement -> ID = . expr)
        >>>
    
    Then, the value of ``lr.lr_after`` might look like this, showing all productions that
    can legally appear next::
    
        >>> lr.lr_after
        [Production(expr -> expr PLUS expr), 
         Production(expr -> expr MINUS expr), 
         Production(expr -> expr TIMES expr), 
         Production(expr -> expr DIVIDE expr), 
         Production(expr -> MINUS expr), 
         Production(expr -> LPAREN expr RPAREN), 
         Production(expr -> NUMBER), 
         Production(expr -> ID)]
        >>>

``lr.lr_before``
    The grammar symbol that appears immediately before the dot (.) or ``None`` if
    at the beginning of the parse.  

``lr.lr_next``
    A link to the next LR item, representing the next stage of the parse.  ``None`` if ``lr``
    is the last LR item.

``LRItem`` instances also support the ``__len__()`` and ``__getitem__()`` special methods.
``len(lr)`` returns the number of items in ``lr.prod`` including the dot (.). ``lr[n]``
returns ``lr.prod[n]``.

It goes without saying that all of the attributes associated with LR
items should be assumed to be read-only.  Modifications will very
likely create a small black-hole that will consume you and your code.

5. LRTable
----------

The ``LRTable`` class represents constructed LR parsing tables on a
grammar.  

``LRTable(grammar, log=None)``
    Create the LR parsing tables on a grammar.  ``grammar`` is an instance of ``Grammar`` and
    ``log`` is a logger object used to write debugging information.  The debugging information
    written to ``log`` is the same as what appears in the ``parser.out`` file created
    by yacc.  By supplying a custom logger with a different message format, it is possible to get
    more information (e.g., the line number in ``yacc.py`` used for issuing each line of
    output in the log).   

An instance ``lr`` of ``LRTable`` has the following attributes.

``lr.grammar``
    A link to the Grammar object used to construct the parsing tables.

``lr.lr_method``
    The LR parsing method used (e.g., ``'LALR'``)

``lr.lr_productions``
    A reference to ``grammar.Productions``.  This, together with ``lr_action`` and ``lr_goto``
    contain all of the information needed by the LR parsing engine.

``lr.lr_action``
    The LR action dictionary that implements the underlying state machine.  The keys of this dictionary are
    the LR states.

``lr.lr_goto``
    The LR goto table that contains information about grammar rule reductions.

``lr.sr_conflicts``
    A list of tuples ``(state,token,resolution)`` identifying all shift/reduce conflicts. ``state`` is the LR state
    number where the conflict occurred, ``token`` is the token causing the conflict, and ``resolution`` is
    a string describing the resolution taken.  ``resolution`` is either ``'shift'`` or ``'reduce'``.

``lr.rr_conflicts``
    A list of tuples ``(state,rule,rejected)`` identifying all reduce/reduce conflicts.  ``state`` is the
    LR state number where the conflict occurred, ``rule`` is the production rule that was selected
    and ``rejected`` is the production rule that was rejected.   Both ``rule`` and ``rejected`` are
    instances of ``Production``.  They can be inspected to provide the user with more information.

``lrtab.bind_callables(dict)``
    This binds all of the function names used in productions to callable objects
    found in the dictionary ``dict``.  During table generation and when reading
    LR tables from files, PLY only uses the names of action functions such as ``'p_expr'``,
    ``'p_statement'``, etc.  In order to actually run the parser, these names
    have to be bound to callable objects.   This method is always called prior to
    running a parser.

6. LRParser
-----------

The ``LRParser`` class implements the low-level LR parsing engine.

``LRParser(lrtab, error_func)``
    Create an LRParser.  ``lrtab`` is an instance of ``LRTable``
    containing the LR production and state tables.  ``error_func`` is the
    error function to invoke in the event of a parsing error.

An instance ``p`` of ``LRParser`` has the following methods:

``p.parse(input=None,lexer=None,debug=0,tracking=0)``
    Run the parser.  ``input`` is a string, which if supplied is fed into the
    lexer using its ``input()`` method.  ``lexer`` is an instance of the
    ``Lexer`` class to use for tokenizing.  If not supplied, the last lexer
    created with the ``lex`` module is used.   ``debug`` is a boolean flag
    that enables debugging.   ``tracking`` is a boolean flag that tells the
    parser to perform additional line number tracking.  

``p.restart()``
    Resets the parser state for a parse already in progress.

7. ParserReflect
----------------

The ``ParserReflect`` class is used to collect parser specification data
from a Python module or object.   This class is what collects all of the
``p_rule()`` functions in a PLY file, performs basic error checking,
and collects all of the needed information to build a grammar.    Most of the
high-level PLY interface as used by the ``yacc()`` function is actually
implemented by this class.

``ParserReflect(pdict, log=None)``
    Creates a ``ParserReflect`` instance. ``pdict`` is a dictionary
    containing parser specification data.  This dictionary typically corresponds
    to the module or class dictionary of code that implements a PLY parser.
    ``log`` is a logger instance that will be used to report error
    messages.

An instance ``p`` of ``ParserReflect`` has the following methods:

``p.get_all()``
    Collect and store all required parsing information.

``p.validate_all()``
    Validate all of the collected parsing information.  This is a seprate step
    from ``p.get_all()`` as a performance optimization.  In order to
    increase parser start-up time, a parser can elect to only validate the
    parsing data when regenerating the parsing tables.   The validation
    step tries to collect as much information as possible rather than
    raising an exception at the first sign of trouble.  The attribute
    ``p.error`` is set if there are any validation errors.  The
    value of this attribute is also returned.

``p.signature()``
    Compute a signature representing the contents of the collected parsing
    data.  The signature value should change if anything in the parser
    specification has changed in a way that would justify parser table
    regeneration.   This method can be called after ``p.get_all()``,
    but before ``p.validate_all()``.

The following attributes are set in the process of collecting data:

``p.start``
    The grammar start symbol, if any. Taken from ``pdict['start']``.

``p.error_func``
    The error handling function or ``None``. Taken from ``pdict['p_error']``.

``p.tokens``
    The token list. Taken from ``pdict['tokens']``.

``p.prec``
    The precedence specifier.  Taken from ``pdict['precedence']``.

``p.preclist``
    A parsed version of the precedence specified.  A list of tuples of the form
    ``(token,assoc,level)`` where ``token`` is the terminal symbol,
    ``assoc`` is the associativity (e.g., ``'left'``) and ``level``
    is a numeric precedence level.

``p.grammar``
    A list of tuples ``(name, rules)`` representing the grammar rules. ``name`` is the
    name of a Python function or method in ``pdict`` that starts with ``"p_"``.
    ``rules`` is a list of tuples ``(filename,line,prodname,syms)`` representing
    the grammar rules found in the documentation string of that function. ``filename`` and ``line`` contain location
    information that can be used for debugging. ``prodname`` is the name of the 
    production. ``syms`` is the right-hand side of the production.  If you have a
    function like this::
    
        def p_expr(p):
            '''expr : expr PLUS expr
                    | expr MINUS expr
                    | expr TIMES expr
                    | expr DIVIDE expr'''
    
    then the corresponding entry in ``p.grammar`` might look like this::
    
        ('p_expr', [ ('calc.py',10,'expr', ['expr','PLUS','expr']),
                     ('calc.py',11,'expr', ['expr','MINUS','expr']),
                     ('calc.py',12,'expr', ['expr','TIMES','expr']),
                     ('calc.py',13,'expr', ['expr','DIVIDE','expr'])
                   ])

``p.pfuncs``
    A sorted list of tuples ``(line, file, name, doc)`` representing all of
    the ``p_`` functions found. ``line`` and ``file`` give location
    information.  ``name`` is the name of the function. ``doc`` is the
    documentation string.   This list is sorted in ascending order by line number.

``p.files``
    A dictionary holding all of the source filenames that were encountered
    while collecting parser information.  Only the keys of this dictionary have
    any meaning.

``p.error``
    An attribute that indicates whether or not any critical errors 
    occurred in validation.  If this is set, it means that that some kind
    of problem was detected and that no further processing should be
    performed.

8. High-level operation
-----------------------

Using all of the above classes requires some attention to detail.  The ``yacc()``
function carries out a very specific sequence of operations to create a grammar.
This same sequence should be emulated if you build an alternative PLY interface.


1. A ``ParserReflect`` object is created and raw grammar specification data is
collected.

2. A ``Grammar`` object is created and populated with information
from the specification data.

3. A ``LRTable`` object is created to run the LALR algorithm over
the ``Grammar`` object.

4. Productions in the LRTable and bound to callables using the ``bind_callables()``
method.

5. A ``LRParser`` object is created from from the information in the
``LRTable`` object.



