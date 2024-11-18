import ply.yacc as yacc
from AnalizadorLexico import tokens


def p_programa(p):
    '''programa : sentencias
                | sentencias programa'''
    
def p_sentencias(p):
  '''sentencias : expression
            | statement'''

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULE expression'''

    # if p[2] == '+':
    #     p[0] = p[1] + p[3]
    # elif p[2] == '-':
    #     p[0] = p[1] - p[3]
    # elif p[2] == '*':
    #     p[0] = p[1] * p[3]
    # elif p[2] == '/':
    #     p[0] = p[1] / p[3]
    # elif p[2] == '%':
    #     p[0] = p[1] % p[3]
  
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

# Variables
def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = p[1]


def p_conditional_if(p):
    'statement : IF condition '
    p[0] = f"if ({p[2]})"


# Condiciones
def p_condition(p):
    '''condition : expression GREATER_THAN expression
                 | expression LESS_THAN expression
                 | expression GREATER_EQ expression
                 | expression LESS_EQ expression
                 | expression EQUALS expression
                 | expression NOT_EQUALS expression'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_switch(p):
    '''statement : SWITCH LPAREN expression RPAREN LBRACE cases default RBRACE'''
    p[0] = f"switch ({p[3]}) {{\n{p[6]}\n{p[7]}\n}}"

def p_cases(p):
    '''cases : cases case
             | case'''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]

def p_case(p):
    '''case : CASE NUMBER COLON statements BREAK SEMICOLON'''
    p[0] = f"case {p[2]}:\n{p[4]}\nbreak;"

def p_default(p):
    '''default : DEFAULT COLON statements
               | empty'''
    if len(p) == 4:
        p[0] = f"default:\n{p[3]}"
    else:
        p[0] = ''

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]

def p_statement_assignment(p):
    '''statement : VARIABLE EQUALS expression SEMICOLON'''
    p[0] = f"{p[1]} = {p[3]};"


def p_empty(p):
    'empty :'
    p[0] = ''





# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: {p.value}")
    else:
        print("Error de sintaxis: entrada inesperada.")


# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('Rast > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)