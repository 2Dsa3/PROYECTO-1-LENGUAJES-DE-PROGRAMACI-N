import ply.lex as lex
import datetime
import subprocess
from pathlib import Path

# Palabras reservadas y tipos de datos
reserved = {
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'for': 'FOR', 'do': 'DO', 'break': 'BREAK',
    'continue': 'CONTINUE', 'public': 'PUBLIC', 'protected': 'PROTECTED', 'private': 'PRIVATE',
    'class': 'CLASS', 'extends': 'EXTENDS', 'implements': 'IMPLEMENTS', 'abstract': 'ABSTRACT',
    'interface': 'INTERFACE', 'final': 'FINAL', 'const': 'CONST', 'null': 'NULL',
    'true': 'TRUE', 'false': 'FALSE', 'void': 'VOID', 'bool': 'BOOL', 'String': 'STRING',
    'int': 'INTEGER', 'double': 'DOUBLE',  # Añadimos 'double' para análisis léxico
    'List': 'LIST', 'Set': 'SET', 'Map': 'MAP', 'Stack': 'STACK', 'Queue': 'QUEUE',
    'Tree': 'TREE', 'Graph': 'GRAPH'  # Añadimos estructuras de datos
}


# Lista de tokens
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LSQUARE', 'RSQUARE', 'COMMA', 'DOT', 'COLON', 'SEMICOLON', 'VARIABLE', 'HASH', 'FLOAT',
    'LINE_COMMENT', 'BLOCK_COMMENT', 'DOC_COMMENT', 'EQUALS', 'NOT_EQUALS', 'GREATER_THAN',
    'LESS_THAN', 'GREATER_EQ', 'LESS_EQ', 'AS', 'IS', 'IS_NOT', 'ASSIGN', 'NULL_ASSIGN',
    'COMPOSED_ASSIGN', 'NEGATION', 'AND', 'OR', 'MODULE', 'INTEGER_DIVIDE', 'INCREMENT',
    'DECREMENT', 'STRING_LITERAL','TYPE_SPECIFIER','NULLABLE'
) + tuple(reserved.values())

# Expresiones regulares para tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_MODULE = r'%'
t_INTEGER_DIVIDE = r'~/'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_GREATER_EQ = r'>='
t_LESS_EQ = r'<='
t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'
t_ASSIGN = r'='
t_COMPOSED_ASSIGN = r'\+=|-=|\*=|/=|%='
t_NULL_ASSIGN = r'\?\?='
t_NEGATION = r'!'
t_AND = r'&&'
t_OR = r'\|\|'
t_QUESTION_MARK = r'\?'


# Comentarios
def t_LINE_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    pass

def t_DOC_COMMENT(t):
    r'///.*|/\*+.*\*+/'
    pass

# Identificación de literales de cadenas
def t_STRING_LITERAL(t):
    r'\'[^\']*\'|"[^"]*"'
    return t

# Aporte David Sumba
### 
# Identificación de variables y palabras reservadas
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t

# A regular expression rule with some action code
def t_FLOAT(t):
    r'\d+\.\d+'
    #t.value = float(t.value) 
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


###

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Aporte David Sumba  

###
# Tipos de datos y variables
def t_TYPE_SPECIFIER(t):
    r'\b(int|double|String|bool|List|Set|Map|dynamic|Object|num)\b'
    t.type = reserved.get(t.value, 'TYPE_SPECIFIER')
    return t

def t_NULLABLE(t):
    r'\w+\?'
    return t
###
# Ignorar espacios y tabs
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    error_msg = f"Illegal character '{t.value[0]}'"
    log_error(error_msg)
    t.lexer.skip(1)

#Aporte Juan Severino 
###
# Funciones para el log
def get_git_user():
    try:
        user_name = subprocess.check_output(['git', 'config', '--get', 'user.name']).strip().decode()
        return user_name
    except subprocess.CalledProcessError:
        return 'unknown_user'

def generate_log_filename():
    now = datetime.datetime.now()
    user_git = get_git_user()
    return f"logs/lexico-{user_git}-{now.strftime('%d%m%Y-%Hh%M')}.txt"

def log_token(token):
    with open(log_filename, 'a') as log_file:
        log_file.write(f"Token: {token.type}, Value: {token.value}, Line: {token.lineno}\n")

def log_error(error_msg):
    with open(log_filename, 'a') as log_file:
        log_file.write(f"ERROR: {error_msg}\n")
###
# Inicializar lexer
lexer = lex.lex()

# Lectura de archivos
def read_dart_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Archivo Dart para analizar
algorithm = 'Algoritmo1.dart'
data = read_dart_file(Path(algorithm))

# Generar log
log_filename = generate_log_filename()

# Encabezado del log
with open(log_filename, 'w') as log_file:
    log_file.write(f"Lex-analyzer started at: {datetime.datetime.now()}\n\n")

# Analizar tokens
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    log_token(tok)

with open(log_filename, 'a') as log_file:
    log_file.write(f"\nLex-analyzer finished at: {datetime.datetime.now()}\n")
