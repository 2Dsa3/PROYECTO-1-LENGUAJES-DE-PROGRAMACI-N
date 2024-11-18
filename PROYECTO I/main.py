import ply.yacc as yacc
from AnalizadorLexico import tokens


def p_asignacion(p):
  'asignacion : NUMBER operador NUMBER'

def p_operador(p):
  '''operador : PLUS
              | MINUS
              | TIMES
              | DIVIDE 
              | MODULE'''
  

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