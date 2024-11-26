import ply.yacc as yacc
from AnalizadorLexico import tokens, generate_log_filename
import datetime


# Definición de las reglas del analizador
def p_program(p):
    """program : statements"""
    p[0] = ('program', p[1])


def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


# Agregar aqui mas formas de statement
def p_statement(p):
    """statement : var_declaration
                 | data_structure
                 | control_structure"""
    p[0] = p[1]


# Reglas para var_declaration
def p_var_declaration(p):
    """var_declaration : VARIABLE ASSIGN expression SEMICOLON
                       | VARIABLE NULL_ASSIGN expression SEMICOLON"""
    p[0] = ('var_declaration', p[1], p[2], p[3])


def p_var_declaration_with_type(p):
    """var_declaration : type VARIABLE ASSIGN expression SEMICOLON"""
    p[0] = ('var_declaration_with_type', p[1], p[2], p[4])


def p_var_declaration_with_bool_type(p):
    """var_declaration : bool_type VARIABLE ASSIGN bool_expression SEMICOLON"""
    p[0] = ('var_declaration_with_bool_type', p[1], p[2], p[4])


def p_var_declaration_with_num_type(p):
    """var_declaration : num_type VARIABLE ASSIGN num_expression SEMICOLON"""
    p[0] = ('var_declaration_with_num_type', p[1], p[2], p[4])


def p_type(p):
    """type : VOID
            | STRING
            | LIST
            | SET
            | MAP
            | STACK
            | QUEUE
            | TREE
            | GRAPH"""
    p[0] = p[1]


def p_bool_type(p):
    """bool_type : BOOL"""
    p[0] = p[1]


def p_num_type(p):
    """num_type : FLOAT
                | INTEGER
                | DOUBLE"""
    p[0] = p[1]


# Reglas para las expresiones
def p_b_expression(p):
    """expression : bool_expression"""
    p[0] = p[1]


# Reglas para las expresiones
def p_n_expression(p):
    """expression : num_expression"""
    p[0] = p[1]


def p_expression_variable(p):
    """expression : VARIABLE"""
    p[0] = ('variable', p[1])


def p_expression_boolean(p):
    """bool_expression : TRUE
                        | FALSE"""
    p[0] = ('boolean', p[1])


def p_expression_numeric(p):
    """num_expression : NUMBER
                    | INTEGER
                    | FLOAT"""
    p[0] = ('numeric', p[1])


def p_bool_expression(p):
    """bool_expression : NEGATION bool_expression
                      | bool_expression AND bool_expression
                      | bool_expression OR bool_expression"""
    p[0] = ('boolean_op', p[2], p[1], p[3])


def p_num_expression(p):
    """num_expression : num_expression PLUS num_expression
                      | num_expression MINUS num_expression
                      | num_expression TIMES num_expression
                      | num_expression DIVIDE num_expression
                      | num_expression INTEGER_DIVIDE num_expression
                      | num_expression MODULE num_expression"""
    p[0] = ('numeric_op', p[2], p[1], p[3])


def p_bool_expression_group(p):
    """bool_expression : LPAREN bool_expression RPAREN"""
    p[0] = p[2]


def p_num_expression_group(p):
    """num_expression : LPAREN num_expression RPAREN"""
    p[0] = p[2]


# Reglas para estructuras de datos
def p_data_structure(p):
    """data_structure : list_structure
                      | map_structure
                      | set_structure"""
    p[0] = p[1]


def p_list_structure(p):
    """list_structure : LSQUARE elements RSQUARE"""
    p[0] = ('list', p[2])


def p_map_structure(p):
    """map_structure : LBRACE key_value_pairs RBRACE"""
    p[0] = ('map', p[2])

def p_set_structure(p):
    """set_structure : LBRACE elements RBRACE"""
    p[0] = ('set', p[2])

def p_elements(p):
    """elements : elements COMMA expression
                | expression"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_key_value_pairs(p):
    """key_value_pairs : key_value_pairs COMMA key_value
                       | key_value"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_key_value(p):
    """key_value : expression COLON expression"""
    p[0] = (p[1], p[3])

#Reglas para la estructuras de control

def p_control_structure(p):
    """control_structure : if_structure
                        | switch_structure"""
    

## regla if
def p_if(p):
    """if_structure : IF LPAREN condition RPAREN LBRACE statement RBRACE"""
    p[0] = f"if ({p[2]})"

#Regla para switch 
def p_switch(p):
    '''switch_structure : SWITCH LPAREN expression RPAREN LBRACE cases default RBRACE'''
    p[0] = f"switch ({p[3]}) {{\n{p[6]}\n{p[7]}\n}}"


def p_condition(p):
    '''condition : expression GREATER_THAN expression
                 | expression LESS_THAN expression
                 | expression GREATER_EQ expression
                 | expression LESS_EQ expression
                 | expression EQUALS expression
                 | expression NOT_EQUALS expression'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_cases(p):
    '''cases : cases case
             | case'''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]

def p_case(p):
    '''case : CASE NUMBER COLON statement BREAK SEMICOLON'''
    p[0] = f"case {p[2]}:\n{p[4]}\nbreak;"

def p_default(p):
    '''default : DEFAULT COLON statement
               | empty'''
    if len(p) == 4:
        p[0] = f"default:\n{p[3]}"
    else:
        p[0] = ''

def p_empty(p):
    'empty :'
    p[0] = ''

def p_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = f"print({p[3]});"

def p_input(p):
    '''statement : INPUT LPAREN expression RPAREN SEMICOLON'''
    p[0] = f"input({p[3]});"
    
# Manejo de errores
def p_error(p):
    error_msg = f"Syntax error at line {p.lineno}: Unexpected token '{p.value}'" if p else "Syntax error in EOF"
    log_error(error_msg)


def log_error(error_msg):
    with open(log_filename, 'a') as log_file:
        log_file.write(f"ERROR: {error_msg}\n")


# Archivo Dart para analizar

algorithm = 'algorithms/Algoritmo2.dart'

log_filename = generate_log_filename('sintactico')

# Construcción del analizador
parser = yacc.yacc()

# Proceso de log
with open(log_filename, 'w', encoding='utf-8') as log_file:
    log_file.write(f"Syntax-analyzer started at: {datetime.datetime.now()}\n\n")

with open(algorithm, 'r') as file:
    content = file.read()
    print(content)
    try:
        result = parser.parse(content)

    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
    print(result)

with open(log_filename, 'a') as log_file:
    log_file.write(f"\nSyntax-analyzer finished at: {datetime.datetime.now()}\n\n")
