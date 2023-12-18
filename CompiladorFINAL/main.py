# ATIVIDADE PRÁTICA - reconhecedor de estruturas em C

from ply import *
import logging

# Tabela de simbolos
# {ID {valor, tipo, contexto}}
simbolos = {}


# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'main': 'MAIN',
    'char': 'CHAR',
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'return': 'RETURN'
    
}

# Demais TOKENS
tokens = [
    'PREPROCESSOR', 'EQUAL_TO','ASSIGN', 'AND', 'OR', 'NOT','INCREMENT', 'DECREMENT', 
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN', 
    'MODULO_ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO','POWER','POWER2', 
    'TERNARY_IF', 'TERNARY_ELSE', 'ADDRESSOF', 'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 
    'GE', 'NOTEQUAL', 'COMMA', 'SEMI', 'INTEGER', 'FLOATNUM', 'DOUBLENUM', 'STRING', 
    'CHARACTER', 'ID', 'SEMICOLON', 'RBRACES', 'LBRACES', 'RBRACKETS', 'LBRACKETS'
] + list(reserved.values())             
""" NEWLINE RETIRADO """

t_ignore = ' \t\n'

def t_REM(t):
    r'REM .*'
    return t

# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_EQUAL_TO = r'=='
t_ASSIGN = r'='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_PLUS_ASSIGN     = r'\+='
t_MINUS_ASSIGN    = r'-='
t_MULTIPLY_ASSIGN = r'\*='
t_DIVIDE_ASSIGN   = r'/='
t_MODULO_ASSIGN   = r'%='
t_TERNARY_IF      = r'\?'
t_TERNARY_ELSE    = r':'
t_PLUS = r'\+'
t_MINUS = r'-'
t_POWER = r'\*\*'
t_POWER2 = r'\^'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RBRACES = r'\}'
t_LBRACES = r'\{'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_SEMICOLON = r'\;'
t_ADDRESSOF = r'\&'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NOTEQUAL = r'!='
t_AND = r'\&&'
t_OR  = r'\|\|'
t_NOT = r'!'
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOATNUM = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_DOUBLENUM = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+)|\d*\.\d+)'
t_STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'
t_CHARACTER = r"'([^'\\\n]|\\.|\\')'"
t_PREPROCESSOR = r'\#(\s)*\w+(\s)*\<.*?\>(\s)*'


def t_COMMENT(t):
    #r'(/\*(.|\n)*?\*/)|(//.*)'
    r'//.*|/\*([^*]|\*[^/])*\*/'
    t.lexer.lineno += t.value.count('\n')

""" def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t """

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# Constroi o analisador léxico
lexer = lex.lex()


# Definece os procedimentos associados as regras de
# produção da gramática (também é quando definimos a gramática)

 
def p_inicio(p):
    '''inicio : INT MAIN LPAREN RPAREN blocoprincipal'''
    print("termino da análise ", p[0], "Símbolos: ", simbolos)


def p_blocoprincipal(p):
    '''blocoprincipal : LBRACES declaracoes comandos RBRACES
                        | LBRACES comandos RBRACES
                        | LBRACES declaracoes RBRACES'''
    print("produção do bloco principal .. ")

def p_declaracoes(p):
    '''declaracoes : tipo ID SEMICOLON
                    | tipo ID SEMICOLON declaracoes
                    | tipo lista_ids SEMICOLON declaracoes
                    | tipo lista_ids SEMICOLON
                    | tipo ID ASSIGN valor SEMICOLON declaracoes
                    | tipo ID ASSIGN valor SEMICOLON
                    | tipo lista_ids ASSIGN valor SEMICOLON declaracoes
                    | tipo lista_ids ASSIGN valor SEMICOLON
                    | tipo ID LBRACKETS INTEGER RBRACKETS SEMICOLON declaracoes
                    | tipo ID LBRACKETS INTEGER RBRACKETS SEMICOLON
                    | tipo ID LBRACKETS RBRACKETS ASSIGN valor SEMICOLON
                    | tipo ID LBRACKETS RBRACKETS ASSIGN valor SEMICOLON declaracoes'''
    tipo = p[1]
    ids = [p[2]] if isinstance(p[2], str) else p[2]
    if len(p) == 9:
        valor = p[6]
    elif len(p) >= 6 and p[3] != '[':
        valor = p[4]
    else:
        valor = None

    for id in ids:
        if id in simbolos:
            print("Erro semântico: variável", id, "já declarada")
            raise Exception(f"Erro semântico: variável '{id}' já declarada")
        else:
            if valor is not None:
                simbolos[id] = {'tipo': valor['tipo'], 'valor': valor['valor'], 'nome': id}
                simbolos[id]['valor'] = valor['valor']
                print("variável adicionada na tabela de símbolos:", id)
            else:
                simbolos[id] = {'tipo': tipo, 'valor': None, 'nome': id}
                print("variável adicionada na tabela de símbolos:", id)
    print("produção de declarações .. ",p[1], p[2])
    
def p_lista_ids(p):
    '''lista_ids : ID
                | lista_ids COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    print("produção de lista de IDs .. ", p[0])
    

def p_tipo(p):
    ''' tipo : INT
            | FLOAT
            | CHAR 
            | DOUBLE'''
    p[0] = p.slice[1].type
    print("Tipo identificado... ", p[0])
    
def p_valor(p):
    '''valor : INTEGER
            | FLOATNUM
            | DOUBLENUM
            | STRING
            | CHARACTER'''
    tipo_token_para_tipo_variavel = {
        'INTEGER': 'INT',
        'FLOATNUM': 'FLOAT',
        'DOUBLENUM': 'DOUBLE',
    }
    tipo_variavel = tipo_token_para_tipo_variavel.get(p.slice[1].type, p.slice[1].type)
    if tipo_variavel == 'INT':
        p[0] = {'tipo': tipo_variavel, 'valor': int(p[1])}
    elif tipo_variavel == 'FLOAT' or tipo_variavel == 'DOUBLE':
        p[0] = {'tipo': tipo_variavel, 'valor': float(p[1])}
    else:
        p[0] = {'tipo': tipo_variavel, 'valor': p[1]}
    print("producao de valor atribuído", p[0])
    
def p_comandos(p):
    '''comandos : comando
                | comando comandos'''
    print("produção de comandos .. ")
    
def p_comando(p):
    '''comando : if_statement
               | while_statement
               | for_statement
               | declaracoes
               | atribuicao
               | printf_statement
               | scanf_statement
               | return_statement
               | expressao_aritmetica SEMICOLON'''
    p[0] = {'tipo': 'comando', 'valor': p[1]}
    print("produção de comando .. ", p[0])
    
def p_if_statement(p):
    '''if_statement : IF LPAREN expressao RPAREN blocoprincipal
                    | IF LPAREN expressao RPAREN comando
                    | IF LPAREN expressao RPAREN blocoprincipal ELSE blocoprincipal'''
    print("produção de if statement .. ")

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expressao RPAREN blocoprincipal'''
    print("produção de while statement .. ")

def p_for_statement(p):
    '''for_statement : FOR LPAREN declaracoes expressao SEMICOLON atribuicao RPAREN blocoprincipal
                    | FOR LPAREN atribuicao comparacao SEMICOLON expressao_aritmetica RPAREN blocoprincipal'''
    p[0] = ('for_statement', p[3], p[4], p[6], p[8])
    print("produção de for statement .. ", p[0])

def p_atribuicao(p):
    '''atribuicao : ID ASSIGN expressao SEMICOLON
                | ID ASSIGN valor SEMICOLON
                | ID PLUS_ASSIGN expressao SEMICOLON
                | ID MINUS_ASSIGN expressao SEMICOLON
                | ID MULTIPLY_ASSIGN expressao SEMICOLON
                | ID DIVIDE_ASSIGN expressao SEMICOLON
                | ID MODULO_ASSIGN expressao SEMICOLON'''
    if p[1] not in simbolos:
        print(f"Erro semântico: variável '{p[1]}' não declarada")
        raise Exception(f"Erro semântico: variável '{p[1]}' não declarada")
    elif p[3] is None:
        print("EXPRESSAO: ",p[1], " ",p[2]," ",p[3])
        print(f"Erro semântico: expressão nula na atribuição '{p[1]}'")
        raise Exception(f"Erro semântico: expressão nula na atribuição '{p[1]}'")
    else:
        if simbolos[p[1]]['tipo'] in ['DOUBLE', 'FLOAT'] and p[3]['tipo'] == 'INT':
            simbolos[p[1]]['valor'] = int(p[3]['valor'])
        elif simbolos[p[1]]['tipo'] == 'INT' and p[3]['tipo'] in ['DOUBLE', 'FLOAT']:
            print(f"Erro semântico: não é possível atribuir um valor não inteiro a uma variável inteira '{p[1]}'")
            raise Exception(f"Erro semântico: não é possível atribuir um valor não inteiro a uma variável inteira '{p[1]}'")
        else:
            simbolos[p[1]]['valor'] = p[3]['valor']
        print(f"Variável '{p[1]}' atualizada na tabela de símbolos: ", simbolos[p[1]])

def p_printf_statement(p):
    '''printf_statement : PRINTF LPAREN STRING COMMA argumentos_printf RPAREN SEMICOLON
                        | PRINTF LPAREN STRING RPAREN SEMICOLON'''
    print("produção de printf statement .. ")

def p_argumentos_printf(p):
    '''argumentos_printf : expressao
                         | argumentos_printf COMMA argumentos_printf'''
    print("produção de argumentos_printf .. ")

def p_scanf_statement(p):
    '''scanf_statement : SCANF LPAREN STRING COMMA ADDRESSOF ID RPAREN SEMICOLON'''
    print("produção de scanf statement .. ")

def p_return_statement(p):
    '''return_statement : RETURN expressao SEMICOLON'''
    print("produção de return statement .. ")

def p_expressao(p):
    '''expressao : valor
                 | comparacao
                 | expressao_logica
                 | expressao_aritmetica
                 | ID '''
    if p.slice[1].type == 'ID':
        if p[1] not in simbolos:
            print(f"Erro semântico: variável '{p[1]}' não declarada")
            raise Exception(f"Erro semântico: variável '{p[1]}' não declarada")
        else:
            p[0] = {'tipo': simbolos[p[1]]['tipo'], 'valor': simbolos[p[1]]['valor'], 'nome': p[1]}
    else:
        p[0] = p[1]
    print("produção de expressão .. ", p[0])

def p_expressao_aritmetica(p):
    '''expressao_aritmetica : termo PLUS termo
                            | termo MINUS termo
                            | termo TIMES termo
                            | termo DIVIDE termo
                            | termo MODULO termo
                            | termo POWER termo
                            | ID INCREMENT 
                            | ID DECREMENT'''
    if len(p) == 3:  # Para INCREMENT e DECREMENT
        if p[1] in simbolos:
            if p.slice[2].type == 'INCREMENT':
                if simbolos[p[1]]['tipo'] == 'INT':
                    simbolos[p[1]]['valor'] = int(simbolos[p[1]]['valor']) + 1
                    p[0] = {'tipo': simbolos[p[1]]['tipo'], 'valor': simbolos[p[1]]['valor'], 'nome': simbolos[p[1]]['nome']}
                elif simbolos[p[1]]['tipo'] == 'FLOAT' or 'DOUBLE':
                    simbolos[p[1]]['valor'] = float(simbolos[p[1]]['valor']) + 1
                    p[0] = {'tipo': simbolos[p[1]]['tipo'], 'valor': simbolos[p[1]]['valor'], 'nome': simbolos[p[1]]['nome']}
            elif p.slice[2].type == 'DECREMENT':
                simbolos[p[1]]['valor'] = float(simbolos[p[1]]['valor']) - 1
                p[0] = {'tipo': simbolos[p[1]]['tipo'], 'valor': simbolos[p[1]]['valor'], 'nome': simbolos[p[1]]['nome']}
        else:
            print(f"Erro semântico: operação '{p[2]}' não suportada para expressões não identificadoras")
            raise Exception(f"Erro semântico: operação '{p[2]}' não suportada para expressões não identificadoras")
    else:
        if p[1] is None or p[3] is None:
            print(f"Erro semântico: expressões nulas na operação '{p[2]}'")
            raise Exception(f"Erro semântico: expressões nulas na operação '{p[2]}'")
        elif p[1]['tipo'] != p[3]['tipo'] and not (p[1]['tipo'] in ['DOUBLE', 'FLOAT'] and p[3]['tipo'] == 'INT'):
            print(f"Erro semântico: tipos incompatíveis na operação '{p[2]}'")
            raise Exception(f"Erro semântico: tipos incompatíveis na operação '{p[2]}'")
        else:
            if p.slice[2].type =='PLUS':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] + p[3]['valor']}
            elif p.slice[2].type =='MINUS':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] - p[3]['valor']}
            elif p.slice[2].type =='TIMES':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] * p[3]['valor']}
            elif p.slice[2].type =='DIVIDE':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] / p[3]['valor']}
            elif p.slice[2].type =='MODULO':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] % p[3]['valor']}
            elif p.slice[2].type =='POWER':
                p[0] = {'tipo': p[1]['tipo'], 'valor': p[1]['valor'] ** p[3]['valor']}
            
            if 'nome' in p[1]:
                simbolos[p[1]['nome']]['valor'] = p[0]['valor']
    

def p_termo(p):
    '''termo : ID
            | INTEGER
            | FLOATNUM
            | DOUBLENUM
            | valor'''
    if isinstance(p[1], dict):
        p[0] = p[1]  # Se for um dicionário, já está no formato correto
    elif isinstance(p[1], int):
        p[0] = {'tipo': 'INT', 'valor': p[1]}
    elif isinstance(p[1], float):
        p[0] = {'tipo': 'FLOAT', 'valor': p[1]}
    else:
        if p[1] not in simbolos:
            print(f"Erro semântico: variável '{p[1]}' não declarada")
            raise Exception(f"Erro semântico: variável '{p[1]}' não declarada")
        else:
            p[0] = {'tipo': simbolos[p[1]]['tipo'], 'valor': simbolos[p[1]]['valor'], 'nome': p[1]}

def p_comparacao(p):
    '''comparacao : expressao EQUAL_TO expressao
                  | expressao LT expressao
                  | expressao GT expressao
                  | expressao LE expressao
                  | expressao GE expressao
                  | expressao NOTEQUAL expressao'''
    print("produção de comparação .. ")

def p_expressao_logica(p):
    '''expressao_logica : expressao AND expressao
                        | expressao OR expressao
                        | NOT expressao'''
    print("produção de expressão lógica .. ")


    

def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    if p:
        print("Erro sintático: token inesperado '%s'" % p.value)
    else:
        print("Erro sintático: fim de arquivo inesperado")


yacc.yacc()

logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)




""" --------------------------------------------------- """
# string de teste
arquivo = './example.c'
with open(arquivo, 'r') as file:
    data = file.read()

# string de teste como entrada do analisador léxico
lexer.input(data)   

# Tokenização
output = ''''''
""" for tok in lexer:
     print(tok)
     output = output + tok.value """


# chama o parser
yacc.parse(data, debug=logging.getLogger())
