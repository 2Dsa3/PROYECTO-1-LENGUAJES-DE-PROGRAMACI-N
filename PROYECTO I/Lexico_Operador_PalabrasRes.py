import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'case':"CASE",
    'for':"FOR",
    'do':"DO",
    'break':"BREAK",
    'continue':"CONTINUE",
    'public':"PUBLIC",
    'protected':"PROTECTED",
    'private':"PRIVATE",
    'class':'CLASS',
    'extends':"EXTENDS",
    'implements':"IMPLEMENTS",
    "abstract":"ABSTRACT",
    'interface':"INTERFACE",
    'final':'FINAL',
    'const':"CONST",
    'null':"NULL",
    'true':"TRUE",
    "false":"FALSE",
    'void':"VOID",
    'bool':"BOOL",
    'string':"STRING",

    # Añade más palabras reservadas según lo necesites
}

class MyLexer(object):
    # List of token names.   This is always required
    tokens = (
       'NUMBER',
       'PLUS', #Aritmeticos
       'MINUS',
       'TIMES',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
       'MODULE',
       "INTEGER_DIVIDE",
       "INCREMENT",##Incremento
       "DECREMENT",
       "VARIABLE",##Variable
       "STRING",
       'EQUALS',  ##Igualdad y relaciones     
        'NOT_EQUALS',   
        'GREATER_THAN',
        'LESS_THAN',   
        'GREATER_EQ',   
        'LESS_EQ', 
        'AS', #Prueba de tipo
        'IS',        
        'IS_NOT', 
        "ASSIGN",##Asignacion
        "NULL_ASSIGN",
        "COMPOSED_ASSIGN",
        "NEGATION",##OPERADORES LOGICOS
        "AND",
        "OR",
        "SEMICOLON",
        "INTEGER",
        "LBRACKETS",
        "RBRACKETS",
        

    

    ) + tuple(reserved.values())

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACKETS = r'\{'
    t_RBRACKETS = r'\}'


    #OPERADORES

    def t_INTEGER(self,t):
        r'int'
        return t

    def t_MODULE(self,t):
        r'\%' 
        return t

    # Regla para INTEGER_DIVIDE (usando ~/ para la división entera)
    def t_INTEGER_DIVIDE(self,t):
        r'\~/'
        return t
    
    def t_INCREMENT(self,t):
        r'\++' 
        return t
    
    def t_DECREMENT(self,t):
        r'\--' 
        return t
    

    def t_EQUALS(self,t):
        r'=='
        return t
    
    def t_NOT_EQUALS(self,t):
        r'!='
        return t
    
    def t_GREATER_EQ(self,t):
        r'>='
        return t
    
    def t_LESS_EQ(self,t):
        r'<='
        return t
    
    def t_GREATER_THAN(self,t):
        r'>'
        return t
    
    def t_LESS_THAN(self,t):
        r'<'
        return t
    
    def t_AS(self,t):
        r'as'
        return t

    def t_IS(self,t):
        r'is'
        return t

    def t_IS_NOT(self,t):
        r'is!'
        return t
    
    def t_ASSIGN(self,t):
        r'='
        return t

    def t_COMPOSED_ASSIGN(self,t):
        r'\+=|-=|\*=|/=|%=|//='
        return t

    def t_NULL_ASSIGN (self,t):
        r'\?\?='
        return t

       
    def t_VARIABLE(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t
    
    def t_NEGATION(self,t):
        r'\!'
        return t
    
    def t_AND(self,t):
        r'\&&'
        return t

    def t_OR(self,t):
        r'\|\|'
        return t
    
    
    def t_STRING(self,t):
        r'\'[a-zA-Z_][a-zA-Z_0-9]*\''
        return t
    
    def t_SEMICOLON(self,t):
        r'\;'
        return t
    
    


    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')  # Verifica si el identificador es una palabra reservada
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)

# Build the lexer and try it out
m = MyLexer()
m.build()           # Build the lexer
m.test("""  int a = 10;
  int b = 3;
  int result;

  result = a - b;
  
  result = a * b; 
  
  result = a ~/ b;

  result = a % b; 
  
  a++; 
  a--;

  bool isEqual = (a == b); 
  bool isNotEqual = (a != b); 
  bool greaterThan = (a > b); 
  bool lessThan = (a < b); 
  bool greaterOrEqual = (a >= b); 
  bool lessOrEqual = (a <= b); 
  String text = 'Dart';
  bool andOperator = (a > b && b > 0); 
  bool orOperator = (a > b || b < 0); 

    if (result > 0) {
        result++;
    } else {
        result--;
    }

   while (result < 3) {
    result++;
  }""")     # Test it
