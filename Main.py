#encoding=utf-8
import re
import sys

reserved = ["PRINT", "BEGIN", "END", "WHILE", "WEND", "IF", "ELSE", "THEN", "AND", "OR", "INPUT", "SUB", "DIM", "AS", "INTEGER", "BOOLEAN", "TRUE", "FALSE", "TYPE", "NOT", "FUNCTION", "CALL"]
PRINT, BEGIN, END, WHILE, WEND, IF, ELSE, THEN, AND, OR, INPUT, SUB, DIM, AS, INTEGER, BOOLEAN, TRUE, FALSE, TYPE, NOT, FUNCTION, CALL= reserved

class Token:
    def __init__(self, tipo, valor):
        self.type = tipo # string
        self.value = valor # integer

    def __repr__(self):
        return "{0} - {1}".format(self.type, self.value)

class Tokenizer:
    def __init__(self, origin, actual):
        self.origin = origin # string, código fonte que sera tokenizado
        self.position = 0 # integer, posição atual que o Tokenizador está separando
        if actual == None:
            self.actual = Token("int", 0) # token, lê o próximo token e atualiza o atributo actual
        else:
            self.actual = Token(actual.type, actual.value)

    def selectNext(self):
        while (self.position < len(self.origin)) and self.origin[self.position] == " ": # se for espaço só pula
            self.position = self.position + 1

        if self.position == len(self.origin):
            self.actual = Token("eof", "eof")

        elif self.origin[self.position].isdigit():
            word = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()): # se for digito vai concatenando
                word = word + self.origin[self.position]
                self.position = self.position + 1

            self.actual = Token("int", int(word))

        elif self.origin[self.position] == '*': # se for mult
            self.actual =  Token("mult", "*")
            self.position = self.position + 1

        elif self.origin[self.position] == '/': # se for div
            self.actual =  Token("div", "/")
            self.position = self.position + 1

        elif self.origin[self.position] == '+': # se for soma
            self.actual =  Token("plus", "+")
            self.position = self.position + 1

        elif self.origin[self.position] == '-': # se for sub
            self.actual = Token("minus", "-")
            self.position = self.position + 1

        elif self.origin[self.position] == '(': # se for abrir par
            self.actual = Token("openpar", "(")
            self.position = self.position + 1

        elif self.origin[self.position] == ')': # se for fechar par
            self.actual = Token("closepar", ")")
            self.position = self.position + 1

        elif self.origin[self.position] == '=': # se for igual
            self.actual = Token("assignment", "=")
            self.position = self.position + 1

        elif self.origin[self.position] == '\n': # se for quebra de linha
            self.actual = Token("breakline", "\n")
            self.position = self.position + 1

        elif self.origin[self.position] == '>': # se for greather than
            self.actual = Token("greaterthan", ">")
            self.position = self.position + 1

        elif self.origin[self.position] == '<': # se for less than
            self.actual = Token("lessthan", "<")
            self.position = self.position + 1

        elif self.origin[self.position] == ',': # se for virgula
            self.actual = Token("comma", ",")
            self.position = self.position + 1

        elif self.origin[self.position].isalpha():

            word = "" #se for palavra vai concatenando, precisa checar se chegou no final
            while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"): 
                word = word + self.origin[self.position]
                self.position = self.position + 1

            word = word.upper()
            
            if word == INTEGER: # se for integer
                self.actual = Token(TYPE, INTEGER)
                #self.position = self.position + 1

            elif word == BOOLEAN: # se for bool
                self.actual = Token(TYPE, BOOLEAN)
                #self.position = self.position + 1

            elif word == TRUE: # se for true
                self.actual = Token(BOOLEAN, True)
                #self.position = self.position + 1
                
            elif word == FALSE: # se for false
                self.actual = Token(BOOLEAN, False)
                #self.position = self.position + 1

            elif word in reserved:
                self.actual = Token(word, word)
                
            else:
                self.actual = Token("identifier", word)
                
        else:
            raise ValueError("Caractere inválido: {}.".format(self.origin[self.position]))

        #print(self.actual)
        return self.actual

class Parser:
    @staticmethod
    def Program():
        listafilhos = []
        while Parser.tokens.actual.type != "eof":
        # while Parser.tokens.actual.type == SUB or Parser.tokens.actual.type == FUNCTION:
            if Parser.tokens.actual.type == SUB:
                listafilhos.append(Parser.SubDec())
            elif Parser.tokens.actual.type == FUNCTION:
                listafilhos.append(Parser.FuncDec())
            while Parser.tokens.actual.type == 'breakline':
                Parser.tokens.selectNext()

        listafilhos.append(FuncCall("MAIN", []))

        return Statements("Stmts", listafilhos)

    def SubDec():
        if Parser.tokens.actual.type == SUB:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "identifier":
                identifier1 = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                params = []
                if Parser.tokens.actual.type == "openpar":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "identifier":
                        identifier2 = Identifier(Parser.tokens.actual.value, [])
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == AS:
                            Parser.tokens.selectNext()
                            tipo1 = Parser.parseType()
                            params.append(VarDec("variável", [identifier2, tipo1]))
                            while Parser.tokens.actual.type == "comma":
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type == "identifier":
                                    identifier3 = Identifier(Parser.tokens.actual.value, [])
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type == AS:
                                        Parser.tokens.selectNext()
                                        tipo2 = Parser.parseType()
                                        params.append(VarDec("variável", [identifier3, tipo2]))


                    if Parser.tokens.actual.type == "closepar":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "breakline":
                            Parser.tokens.selectNext()
                            stmts = []
                            while Parser.tokens.actual.type != END:
                                node = Parser.Statement()
                                if node != None:
                                    stmts.append(node)
                                if Parser.tokens.actual.type == "breakline":
                                    Parser.tokens.selectNext()

                            if Parser.tokens.actual.type == END:
                                params.append(Statements("stmts", stmts))### stmts
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type == SUB:
                                    Parser.tokens.selectNext()

                return SubDec(identifier1.value, params)

    def FuncDec():
        if Parser.tokens.actual.type == "FUNCTION":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "identifier":
                identifier1 = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                params = []
                if Parser.tokens.actual.type == "openpar":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "identifier":
                        identifier2 = Identifier(Parser.tokens.actual.value, [])
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == AS:
                            Parser.tokens.selectNext()
                            tipo1 = Parser.parseType()
                            params.append(VarDec("variável", [identifier2, tipo1]))
                            while Parser.tokens.actual.type == "comma":
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type == "identifier":
                                    identifier3 = Identifier(Parser.tokens.actual.value, [])
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type == AS:
                                        Parser.tokens.selectNext()
                                        tipo2 = Parser.parseType()
                                        params.append(VarDec("variável", [identifier3, tipo2]))


                    if Parser.tokens.actual.type == "closepar":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == AS:
                            Parser.tokens.selectNext()
                            tipo3 = Parser.parseType()
                            if Parser.tokens.actual.type == "breakline":
                                Parser.tokens.selectNext()
                                stmts = []
                                while Parser.tokens.actual.type != END:
                                    node = Parser.Statement()
                                    if node != None:
                                        stmts.append(node)
                                    if Parser.tokens.actual.type == "breakline":
                                        Parser.tokens.selectNext()

                                if Parser.tokens.actual.type == END:
                                    params.append(Statements("stmts", stmts))### stmts
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type == "FUNCTION":
                                        Parser.tokens.selectNext()

        listona = [tipo3] + params
        return FuncDec(identifier1.value, listona)

    @staticmethod
    def Statement():
        if Parser.tokens.actual.type == "identifier":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "assignment":
                Parser.tokens.selectNext()
                right = Parser.RelExpression()
                node = Assignment("=", [identifier, right])
                return node

            else:
                raise ValueError('Esperava-se uma atribuição com "=", porém foi encontrado {}'.format(Parser.tokens.actual.value))

        elif Parser.tokens.actual.type == PRINT:
            Parser.tokens.selectNext()
            left = Parser.RelExpression()
            node = Print(PRINT, [left])
            return node

        elif Parser.tokens.actual.type == WHILE:
            Parser.tokens.selectNext()
            left = Parser.RelExpression()
            right = Statements('Statements', [])
            if Parser.tokens.actual.type == "breakline":
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != WEND and Parser.tokens.actual.type != "eof":
                    right.children.append(Parser.Statement())
                    if Parser.tokens.actual.type == "breakline":
                        Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == WEND:
                    Parser.tokens.selectNext()
                    return WhileOp("While", [left, right])

                else:
                    raise ValueError('Esperava-se um "WEND", porém foi encontrado {}'.format(Parser.tokens.actual.value))
                
        elif Parser.tokens.actual.type == IF:
            Parser.tokens.selectNext()
            node = [Parser.RelExpression()]
            left = []
            right = []
            if Parser.tokens.actual.type == THEN:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "breakline":
                    Parser.tokens.selectNext()
                    while Parser.tokens.actual.type != END and Parser.tokens.actual.type != ELSE and Parser.tokens.actual.type != "eof":
                        left.append(Parser.Statement())
                        if Parser.tokens.actual.type == "breakline":
                            Parser.tokens.selectNext()
                    node.append(Statements("Statements", left))

                    if Parser.tokens.actual.type == ELSE:
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "breakline":
                            Parser.tokens.selectNext()
                            while Parser.tokens.actual.type != END and Parser.tokens.actual.type != "eof":
                                right.append(Parser.Statement())
                                if Parser.tokens.actual.type == "breakline":
                                    Parser.tokens.selectNext()
                            node.append(Statements("Statements", right))

                    if Parser.tokens.actual.type == END:
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == IF:
                            Parser.tokens.selectNext()
                            
                            return IfOp("If", node)

                        else:
                            raise ValueError('Esperava-se um "IF", porém foi encontrado {}'.format(Parser.tokens.actual.value))
                    else:
                        raise ValueError('Esperava-se um "END", porém foi encontrado {}'.format(Parser.tokens.actual.value))

            else:
                raise ValueError('Esperava-se um "THEN", porém foi encontrado {}'.format(Parser.tokens.actual.value))
        
        elif Parser.tokens.actual.type == DIM:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "identifier":
                identifier = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == AS:
                    Parser.tokens.selectNext()
                    tipo = Parser.parseType()
                    return VarDec("variável", [identifier, tipo])

        elif Parser.tokens.actual.type == "CALL":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "identifier":
                identifier = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "openpar":
                    Parser.tokens.selectNext()
                    nodes = []
                    while Parser.tokens.actual.type != "closepar":
                        nodes.append(Parser.RelExpression())
                        if Parser.tokens.actual.type == "comma":
                            Parser.tokens.selectNext()
                    
                    if Parser.tokens.actual.type == "closepar":
                        Parser.tokens.selectNext()
                        return FuncCall(identifier.value, nodes)

        else:
            return NoOp()

    def RelExpression():
        left = Parser.parseExpression()
        if Parser.tokens.actual.value == "=":
            Parser.tokens.selectNext()
            right = Parser.parseExpression()
            return BinOp("=", [left, right])
            
        elif Parser.tokens.actual.value == ">":
            Parser.tokens.selectNext()
            right = Parser.parseExpression()
            return BinOp(">", [left, right])

        elif Parser.tokens.actual.value == "<":
            Parser.tokens.selectNext()
            right = Parser.parseExpression()
            return BinOp("<", [left, right])

        else:
            return left
        #    raise ValueError('Esperava-se comparador "=" ou ">" ou "<", porém foi encontrado {}'.format(Parser.tokens.actual.value))

    def parseExpression():
        left = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == OR:
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("+", [left, right])
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("-", [left, right])
            elif Parser.tokens.actual.type == OR:
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp(OR, [left, right])
        return left

    def parseTerm():
        left = Parser.parseFactor()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div" or Parser.tokens.actual.type == AND:
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp("*", [left, right])
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp("/", [left, right])
            elif Parser.tokens.actual.type == AND:
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp(AND, [left, right])
        return left

    def parseFactor(): 
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            left = IntVal(res, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "openpar":
            Parser.tokens.selectNext()
            left = Parser.RelExpression()
            if Parser.tokens.actual.type == "closepar":
                Parser.tokens.selectNext()
            else:
                raise ValueError('Esperava-se um fecha parênteses e foi encontrado um {}.'.format(Parser.tokens.actual.type))

        elif Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == NOT:
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("+", [left])
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("-", [left])
            elif Parser.tokens.actual.type == NOT:
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp(NOT, [left])
        
        elif Parser.tokens.actual.type == "identifier":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            nodes = []
            if Parser.tokens.actual.type == "openpar":
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != "closepar":
                    nodes.append(Parser.RelExpression())
                    if Parser.tokens.actual.type == "comma":
                        Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == "closepar":
                    Parser.tokens.selectNext()
                    return FuncCall(identifier.value, nodes)
            else:         
                return identifier

        elif Parser.tokens.actual.type == INPUT:
            Parser.tokens.selectNext()
            return Input('', [])

        elif Parser.tokens.actual.type  == BOOLEAN:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return BoolVal(value, [])

        else:
            raise ValueError('Token inválido: {}'.format(Parser.tokens.actual.value))
        
        return left

    def parseType():
        if Parser.tokens.actual.type == TYPE:
            if Parser.tokens.actual.value == INTEGER:
                Parser.tokens.selectNext()
                return Type(INTEGER, [])

            if Parser.tokens.actual.value == BOOLEAN:
                Parser.tokens.selectNext()
                return Type(BOOLEAN, [])

    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.Program()
        # if Parser.tokens.actual.type == 'breakline':
        #     Parser.tokens.selectNext()
        # if Parser.tokens.actual.type != 'eof':
        #     raise ValueError('Entrada inválida. Último token não é o EOF. {}: {}'.format(Parser.tokens.actual.type, Parser.tokens.actual.value))
        
        return res

class PrePro():

    def filter(entrada):
        filtro = entrada.replace('\\n', '\n')
        filtro = re.sub("'.*\n", "\n", filtro) #para arquivos
        #filtro = re.sub("'.*\r", "\n", filtro) #para arquivos
        #filtro = re.sub("'.*", "", filtro) #apenas para o meu terminal
        return filtro

class Assembler:
    stringf = ""

    @staticmethod
    def AddString(string):
        Assembler.stringf += string + "\n"

    @staticmethod
    def WriteFile():
        inicio = """; constantes 
SYS_EXIT equ 1 
SYS_READ equ 3 
SYS_WRITE equ 4 
STDIN equ 0 
STDOUT equ 1 
True equ 1
False equ 0

segment .data

segment .bss ; variaveis
  res RESB 1


section .text 
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False  
  JMP binop_exit

binop_true:
  MOV EBX, True
binop_exit:
  RET


_start :

PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

"""

        fim = """; interrupcao de saida
        POP EBP
        MOV EAX, 1
        INT 0x80
        """
        with open ("output.nasm", 'w') as file:
                file.write(inicio + Assembler.stringf + fim)
        
class SymbolTable(): #agora valor é [valor, tipo]
    def __init__(self, anterior=None):
        self.table = {}
        self.anterior = anterior

    def getter(self, chave):
        if chave in self.table.keys():
            tupla = self.table[chave]
            #if tupla[0] == None:
            #    try:
            #        tupla = tuple(self.anterior.getter(chave))
            #    except:
            #        raise ValueError("Falha ao tentar fazer recursão: {}".format(tupla[0]))
                
            return tupla

        elif self.anterior != None:
            tupla = self.anterior.getter(chave)
            return tupla
            
        else:
            raise ValueError("Chave {} não localizada na Tabela de Símbolos".format(chave))
    
    def setter(self, chave, valor): #((nome da variável, [tipo, "TYPE"]), value)
        if chave in self.table.keys():
            self.table[chave][0] = valor
        else:
            raise ValueError("Chave {} não existe na Tabela de Símbolos".format(chave))
        return

    def creator(self, chave, tipo):
        self.shift += 4
        if chave in self.table.keys():
            raise ValueError("Chave {} já existe na Tabela de Símbolos".format(chave))
        else:
            self.table[chave] = [None, tipo, self.shift]
            return

class Node():
    i = 0
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
    
    def Evaluate(self, ST):
        pass

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

class BinOp(Node): #2 filhos, binary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        left = self.children[0].Evaluate(ST)
        Assembler.AddString("PUSH EBX")
        right = self.children[1].Evaluate(ST)
        Assembler.AddString("POP EAX")

        if self.value == "+":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("ADD EAX, EBX")
                Assembler.AddString("MOV EBX, EAX")
                return (left[0] + right[0], INTEGER)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

        elif self.value == "-":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("SUB EAX, EBX")
                Assembler.AddString("MOV EBX, EAX")
                return (left[0] - right[0], INTEGER)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

        elif self.value == "*":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("IMUL EBX")
                Assembler.AddString("MOV EBX, EAX")################
                return (left[0] * right[0], INTEGER)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

        elif self.value == "/":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("IDIV EBX")
                Assembler.AddString("MOV EBX, EAX")##############
                return (left[0] // right[0], INTEGER)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

        elif self.value == "=":
            if(left[1] == right[1]):
                Assembler.AddString("CMP EAX, EBX")
                Assembler.AddString("CALL binop_je")
                return ((left[0] == right[0]), BOOLEAN)
            else:
                raise ValueError ("Apenas operações com variáveis do mesmo tipo são permitidas")

        elif self.value == AND:
            if(left[1] == BOOLEAN and right[1] == BOOLEAN):
                Assembler.AddString("AND EBX, EAX")
                return (left[0] and right[0], BOOLEAN)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo BOOLEAN são permitidas.")

        elif self.value == OR:
            if(left[1] == BOOLEAN and right[1] == BOOLEAN):
                Assembler.AddString("OR EBX, EAX")
                return (left[0] or right[0], BOOLEAN)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo BOOLEAN são permitidas.")

        elif self.value == ">":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("CMP EAX, EBX")
                Assembler.AddString("CALL binop_jg")
                return (left[0] > right[0], BOOLEAN)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

        elif self.value == "<":
            if(left[1] == INTEGER and right[1] == INTEGER):
                Assembler.AddString("CMP EAX, EBX")
                Assembler.AddString("CALL binop_jl")
                return (left[0] < right[0], BOOLEAN)
            else:
                raise ValueError ("Para esta operação, apenas variáveis com tipo INTEGER são permitidas.")

class UnOp(Node): #1 filho, unary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        child = self.children[0].Evaluate(ST)
        
        if child[1] == INTEGER:
            if self.value == "+":
                Assembler.AddString("ADD EBX, 0")
                return (+ child[0], INTEGER)

            elif self.value == "-":
                Assembler.AddString("MOV EAX, {}".format(child[0]))
                Assembler.AddString("MOV EBX, -1")
                Assembler.AddString("IMUl EBX")
                Assembler.AddString("MOV EBX, EAX")
                return (- child[0], INTEGER)

        elif child[1] == BOOLEAN:
            if self.value == NOT:
                Assembler.AddString("NEG EBX")
                return (not child[0], BOOLEAN)

class WhileOp(Node): 
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        Assembler.AddString("LOOP_{}:".format(self.id))
        left = self.children[0].Evaluate(ST)
        if left[1] != BOOLEAN:
            raise ValueError ("Para esta operação, apenas variáveis do tipo BOOLEAN são permitidas.")

        Assembler.AddString("CMP EBX, False")
        Assembler.AddString("JE EXIT_{}".format(self.id))
        right = self.children[1].Evaluate(ST)

        Assembler.AddString("JMP LOOP_{}".format(self.id))
        Assembler.AddString("EXIT_{}:".format(self.id))

class IfOp(Node): 
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        Assembler.AddString("If_{}:".format(self.id))
        left = self.children[0].Evaluate(ST)
        Assembler.AddString("CMP EBX, False")
        if left[1] != BOOLEAN:
            raise ValueError ("Para esta operação, apenas variáveis do tipo BOOLEAN são permitidas.")
        else:
            if len(self.children) == 3:
                Assembler.AddString("JE Else_{}".format(self.id))
            else:
                Assembler.AddString("JE EndIf_{}".format(self.id))
                
            self.children[1].Evaluate(ST)
            Assembler.AddString("JMP EndIf_{}".format(self.id))
 
            if len(self.children) == 3:
                Assembler.AddString("Else_{}:".format(self.id))
                self.children[2].Evaluate(ST)

            Assembler.AddString("EndIf_{}:".format(self.id))
            

class IntVal(Node): #0 filhos, int value
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        Assembler.AddString("MOV EBX, {}".format(self.value))
        return (self.value, INTEGER)

class Input(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        entrada = input('>>')
        return (int(entrada), INTEGER)

class NoOp(Node): #0 filhos, dummy
    def __init__(self):
        self.id = Node.newId()
        pass

    def Evaluate(self, ST):
        pass

class Identifier(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        Assembler.AddString("MOV EBX, [EBP-{}]".format(ST.getter(self.value)[2]))
        st = ST.getter(self.value)
        return st 

class Assignment(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        tipo = ST.getter(self.children[0].value)[1] #Declaração -> (nome da variável, [tipo, "TYPE"])
        tupla = self.children[1].Evaluate(ST) #variável (valor, tipo)
        if tipo == tupla[1]:
            Assembler.AddString("MOV [EBP-{}], EBX".format(ST.getter(self.children[0].value)[2]))
            ST.setter(self.children[0].value, tupla[0]) #(nome da variável, value)
        else:
            raise ValueError ("Variável não compatível com o tipo declarado. {}, {}".format(tipo, tupla[1]))

class Statements(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        for filho in self.children:
            filho.Evaluate(ST) #vai dando evaluate em cada filho statement do nó program
            
class Print(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        print(self.children[0].Evaluate(ST)[0])
        Assembler.AddString("PUSH EBX")
        Assembler.AddString("CALL print")
        Assembler.AddString("POP EBX")

class Type(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        return (self.value, "TYPE")

class BoolVal(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        Assembler.AddString("MOV EBX,", self.value)
        return (self.value, BOOLEAN)

class VarDec(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
        self.id = Node.newId()

    def Evaluate(self, ST):
        ST.creator(self.children[0].value, self.children[1].Evaluate(ST)[0])

class FuncCall(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        novaST = SymbolTable(ST)
        funcDec, tipo = novaST.getter(self.value)
        if tipo == FUNCTION:
            #Confirma se a qtd de filhos é a mesma tirando tipo (0) e stmts (-1), m = n-2
            vardecs = funcDec.children[1:-1] #Apenas os vardecs
            if len(vardecs) == len(self.children):
                novaST.creator(self.value, funcDec.children[0].Evaluate(novaST)[0])
                for i in range(len(vardecs)):
                    if vardecs[i].children[1].value == self.children[i].Evaluate(novaST)[1]: #comparando os tipos
                        vardecs[i].Evaluate(novaST)
                        novaST.setter(vardecs[i].children[0].value, self.children[i].Evaluate(novaST)[0])
            funcDec.children[-1].Evaluate(novaST) ### pega nó statements
            return novaST.getter(self.value)#Evaluate de todos os statements de acordo com a ST recém criada.
        
        elif tipo == SUB:
            #Confirma se a qtd de filhos é a mesma tirando stmts (-1)
            vardecs = funcDec.children[:-1] #Apenas os vardecs
            if len(vardecs) == len(self.children):
                for i in range(len(vardecs)):
                    vardecs[i].Evaluate(novaST)
                    novaST.setter(vardecs[i].children[0].value, self.children[i].Evaluate(novaST)[0])
            funcDec.children[-1].Evaluate(novaST) ### pega nó statements
            
class FuncDec(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
       ST.creator(self.value, FUNCTION)
       ST.setter(self.value, self)

class SubDec(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        ST.creator(self.value, SUB)
        ST.setter(self.value, self)
        
def main():
    #try:
        #entrada  = input("Digite o que deseja calcular: ")
        arquivo = 'expressao.vbs' #sys.argv[1]
        teste = 'teste.vbs'
        with open (sys.argv[1], 'r') as file: #sys.argv[1], 'r') as file:
            entrada = file.read()# + "\n"
            
        codigo = PrePro.filter(entrada).rstrip() #apaga qualquer coisa que estiver no fim da string, tipo espaço
        res = Parser.run(codigo)
        ST = SymbolTable()
        res.Evaluate(ST)

    #except Exception as ex:
    #    print(ex)

if  __name__ =='__main__':main()
