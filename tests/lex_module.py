# lex_module.py
#

import ply.lex as lex
import lex_module_import
lex.lex(module=lex_module_import)
lex.runmain(data="3+4")
