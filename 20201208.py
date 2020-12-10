import sys
import ply.lex as lex

import ply.yacc as yacc

tokens =(
'NAME','NUMBER',
'PLUS','MINUS','TIMES','DIVIDE','EQUALS','POWER',
'LPAREN','RPAREN',
)
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_POWER  = r'\^'


t_NAME   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" %t.value)
        t.value=0
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
def t_error(t):
    print("Illegal character '%s'"%t.value[0])
    t.lexer.skip(1)
lexer = lex.lex()
lexer.input('10+2*5/(2+5)/2')
while True:
    tok=lexer.token()
    if not tok:
        break  #No more input
    print(tok)
def p_binary_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression POWER expression
       term       : term TIMES factor
                  | term DIVIDE factor
                  
                  '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] =='^':
        p[0]=p[1]**p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    
def p_expression_term(p):
    'expression : term'
    p[0]=p[1]

def p_term_factor(p):
    'term : factor'
    p[0]=p[1]
def p_factor_num(p):
    'factor : NUMBER'
    p[0]=p[1]
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0]=p[2]
def p_error(p):
    print("Syntax error in input!")
#Bulid the parser
parser =yacc.yacc()
while True:
    try:
        s=input('calc > ')
    except EOFError:
        break
    if not s: continue
    result =parser.parse(s)
    print(result)