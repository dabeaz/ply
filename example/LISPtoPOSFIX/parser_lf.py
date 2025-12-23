import ply.lex as lex
import ply.yacc as yacc

# Tokenizer
# Lista com nome dos tokens
tokens = (
    "ID", 
    "NUMERO",
    "MAIS",
    "MENOS",
    "VEZES",
    "DIVIDIR",
    "ABRE_PAREN",
    "FECHA_PAREN",
)

# Expressões regulares para os tokens
# t_ é um prefixo especial (palavra reservada) que indica que a função é um token

t_MAIS = r"\+"
t_MENOS = r"-"  # O sinal de menos é um token separado para evitar ambiguidade
t_VEZES = r"\*"
t_DIVIDIR = r"/"  # O sinal de divisão é um token separado para evitar ambiguidade
t_ABRE_PAREN = r"\("
t_FECHA_PAREN = r"\)"


# Função para tratar números
def t_NUMERO(t):
    r'-?\d+(\.\d+)?'
    t.value = int(t.value) # Considera positivo ou negativo e float
    return t

# Função para tratar ID
def t_ID(t):
    r"-?[a-zA-Z]+"  # Apenas letras do alfabeto portugues (podendo ser negativo)
    return t

# Ignorar espaços em branco
t_ignore = " \t"

# Ignorar comentários
def t_COMENTARIO(t):
    r'\#.*'
    pass

# Numero da linha
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(
        t.value
    )  # Incrementa o número da linha para cada nova linha encontrada
    # lexer é um objeto global que contém informações sobre o estado do analisador léxico
    # lineno é um atributo de lexer que armazena o número da linha atual


# Tratamento de erro
def t_error(t):
    print("O caractere ilegal '%s' foi pulado" % t.value[0])
    t.lexer.skip(1)  # Pula o caractere ilegal

# Construir o lexer
lexer = lex.lex()

####################
#  Classes Tree    #
####################
####################
# Não interferem   #
# Na análise       #
# É só para arvore #
####################
class ASTNode:
    pass

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.op} {self.left} {self.right})"

class IdNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)
    
def print_tree(node, indent="", is_right=False):
    if isinstance(node, BinaryOpNode):
        op_str = f"{indent}{'└─' if is_right else '├─'}{node.op}"
        print(op_str)
        new_indent = indent + ("   " if is_right else "│  ")
        print_tree(node.left, new_indent, False)
        print_tree(node.right, new_indent, True)
    elif isinstance(node, IdNode) or isinstance(node, NumberNode):
        node_str = f"{indent}{'└─' if is_right else '├─'}{node}"
        print(node_str)
        
def tradutor_toposfix(node):
    if isinstance(node, BinaryOpNode):
        left_expr = tradutor_toposfix(node.left)
        right_expr = tradutor_toposfix(node.right)
        return f"{left_expr} {right_expr} {node.op}"
    elif isinstance(node, IdNode):
        return node.name
    elif isinstance(node, NumberNode):
        return str(node.value)

##################
# --- Parser --- #
##################

# Regras de produção
def p_E_binop(p):
    '''E : ABRE_PAREN MAIS E E FECHA_PAREN
         | ABRE_PAREN MENOS E E FECHA_PAREN
         | ABRE_PAREN VEZES E E FECHA_PAREN
         | ABRE_PAREN DIVIDIR E E FECHA_PAREN'''
    p[0] = BinaryOpNode(p[2], p[3], p[4])

def p_E_id(p):
    'E : ID'
    p[0] = IdNode(p[1])

def p_E_numero(p):
    'E : NUMERO'
    p[0] = NumberNode(p[1])

def p_error(p):
    print(f'Erro de sintaxe: {p.value!r}')

# Construir o parser
parser = yacc.yacc()

# Função para analisar a entrada do arquivo input.txt
arquivo = open('LISPtoPOSFIX/input.txt', 'r')
entrada = arquivo.read()
arquivo.close()

# Chama o parser para entrada lida 
ast = parser.parse(entrada)
print("Entrada: %s\nÁrvore:" % ast)
# Imprime a árvore
print_tree(ast)
# Imprime a expressão pós-fixa
print("Pósfixada: %s" % tradutor_toposfix(ast))

