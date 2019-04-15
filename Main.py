import re
import sys

reserved = ["PRINT", "BEGIN", "END", "WHILE", "WEND", "IF", "ELSE", "THEN", "AND", "OR", "INPUT"]
PRINT, BEGIN, END, WHILE, WEND, IF, ELSE, THEN, AND, OR, INPUT = reserved

class Token:
    def __init__(self, tipo, valor):
        self.type = tipo # string
        self.value = valor # integer

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

        elif self.origin[self.position] == '>': # se for quebra de linha
            self.actual = Token("greaterthan", ">")
            self.position = self.position + 1

        elif self.origin[self.position] == '<': # se for quebra de linha
            self.actual = Token("lessthan", "<")
            self.position = self.position + 1

        elif self.origin[self.position].isalpha():
            
            word = "" #se for palavra vai concatenando, precisa checar se chegou no final
            while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"): 
                word = word + self.origin[self.position]
                self.position = self.position + 1

            word = word.upper()
            if word in reserved:
                self.actual = Token(word, word)
            
            else:
                self.actual = Token("identifier", word)

        else:
            raise ValueError("Caractere inválido: {}.".format(self.origin[self.position]))

        return self.actual

class Parser:
    @staticmethod
    def Statements():
        listafilhos = []
        while Parser.tokens.actual.type != END and Parser.tokens.actual.type != WEND and Parser.tokens.actual.type != ELSE and Parser.tokens.actual.type != "eof":
            node = Parser.Statement() 
            if node != None:
                listafilhos.append(node)
                if Parser.tokens.actual.type == "breakline":
                    Parser.tokens.selectNext()
                #else:
                #    raise ValueError('Esperava-se token "\\n", porém foi encontrado {}.'.format(Parser.tokens.actual.value))
        
        return Statements("Statements", listafilhos)

    @staticmethod
    def Statement():
        if Parser.tokens.actual.type == "identifier":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "assignment":
                Parser.tokens.selectNext()
                left = Parser.parseExpression()
                node = Assignment("=", [identifier, left])
                if Parser.tokens.actual.type == "breakline":#////////////////////////////////////////////////
                    Parser.tokens.selectNext()
                return node

            else:
                raise ValueError('Esperava-se uma atribuição com "=", porém foi encontrado {}'.format(Parser.tokens.actual.value))

        elif Parser.tokens.actual.type == PRINT:
            Parser.tokens.selectNext()
            left = Parser.parseExpression()
            node = Print(PRINT, [left])
            if Parser.tokens.actual.type == "breakline":#////////////////////////////////////////////////
                Parser.tokens.selectNext()
            return node

        elif Parser.tokens.actual.type == WHILE:
            Parser.tokens.selectNext()
            left = Parser.RelExpression() 
            if Parser.tokens.actual.type == "breakline": #breakline se quiser
                Parser.tokens.selectNext()
            right = Parser.Statements()
            if Parser.tokens.actual.type == WEND:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "breakline":#////////////////////////////////////////////////
                    Parser.tokens.selectNext()
                return WhileOp("While", [left, right])
            else:
                raise ValueError('Esperava-se um "WEND", porém foi encontrado {}'.format(Parser.tokens.actual.value))
            
        elif Parser.tokens.actual.type == IF:
            Parser.tokens.selectNext()
            node = Parser.RelExpression()
            left = None
            right = None
            if Parser.tokens.actual.type == THEN:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "breakline": #breakline se quiser
                    Parser.tokens.selectNext()
                left = Parser.Statements() #Faz node if com ele
            else:
                raise ValueError('Esperava-se um "THEN", porém foi encontrado {}'.format(Parser.tokens.actual.value))

            if Parser.tokens.actual.type == ELSE:
                Parser.tokens.selectNext()
                right = Parser.Statements()
            
            if Parser.tokens.actual.type == END:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == IF:
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "breakline":
                        Parser.tokens.selectNext()
                    return IfOp("If", [node, left, right])

                else:
                    raise ValueError('Esperava-se um "IF", porém foi encontrado {}'.format(Parser.tokens.actual.value))
            else:
                raise ValueError('Esperava-se um "END", porém foi encontrado {}'.format(Parser.tokens.actual.value))

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
            raise ValueError('Esperava-se comparador "=" ou ">" ou "<", porém foi encontrado {}'.format(Parser.tokens.actual.value))

    def parseTerm():
        left = Parser.parseFactor()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div" or Parser.tokens.actual.type == "and":
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp("*", [left, right])
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp("/", [left, right])
            elif Parser.tokens.actual.type == "and":
                Parser.tokens.selectNext()
                right =  Parser.parseFactor()
                left = BinOp("and", [left, right])

        return left

    def parseExpression():
        left = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "or":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("+", [left, right])
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("-", [left, right])
            elif Parser.tokens.actual.type == "or":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("or", [left, right])

        return left

    def parseFactor(): 
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            left = IntVal(res, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "openpar":
            Parser.tokens.selectNext()
            left = Parser.parseExpression()
            if Parser.tokens.actual.type == "closepar":
                Parser.tokens.selectNext()
            else:
                raise ValueError('Esperava-se um fecha parênteses e foi encontrado um {}.'.format(Parser.tokens.actual.type))

        elif Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "not":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("+", [left])
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("-", [left])
            else:
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("not", [left])
        
        elif Parser.tokens.actual.type == "identifier":
            res = Parser.tokens.actual.value
            node = Identifier(res, [])
            Parser.tokens.selectNext()
            return node

        elif Parser.tokens.actual.type == INPUT:
            Parser.tokens.selectNext()
            return Input('', [])
        
        else:
            raise ValueError('Token inválido: {}'.format(Parser.tokens.actual.value))
        
        return left

    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.Statements()
        if Parser.tokens.actual.type != 'eof':
            raise ValueError('Entrada inválida. Último token não é o EOF.')
        
        return res

class PrePro():

    def filter(entrada):
        filtro = entrada.replace('\\n', '\n')
        filtro = re.sub("'.*\n", "\n", filtro) #para arquivos
        #filtro = re.sub("'.*\r", "\n", filtro) #para arquivos
        #filtro = re.sub("'.*", "", filtro) #apenas para o meu terminal
        return filtro

        
class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, chave):
        if chave in self.table.keys():
            res = self.table.get(chave)
            return res

        else:
            raise ValueError("Chave {} não localizada na Tabela de Símbolos".format(chave))
    
    def setter(self, chave, valor):
        self.table.update({chave: valor})

class Node():
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
    
    def Evaluate(self, ST):
        pass

class BinOp(Node): #2 filhos, binary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        if self.value == "+":
            return self.children[0].Evaluate(ST) + self.children[1].Evaluate(ST)

        elif self.value == "-":
            return self.children[0].Evaluate(ST) - self.children[1].Evaluate(ST)

        elif self.value == "*":
            return self.children[0].Evaluate(ST) * self.children[1].Evaluate(ST)

        elif self.value == "/":
            return self.children[0].Evaluate(ST) // self.children[1].Evaluate(ST)
    
        elif self.value == "=":
            return self.children[0].Evaluate(ST) == self.children[1].Evaluate(ST)

        elif self.value == "and":
            return self.children[0].Evaluate(ST) and self.children[1].Evaluate(ST)

        elif self.value == "or":
            return self.children[0].Evaluate(ST) or self.children[1].Evaluate(ST)
    
        elif self.value == ">":
            return self.children[0].Evaluate(ST) > self.children[1].Evaluate(ST)
    
        elif self.value == "<":
            return self.children[0].Evaluate(ST) < self.children[1].Evaluate(ST)
    
        else:
            raise ValueError ("Apenas operações com variáveis do mesmo tipo são permitidas")

class UnOp(Node): #1 filho, unary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        if self.value == "+":
            return + self.children[0].Evaluate(ST)

        elif self.value == "-":
            return - self.children[0].Evaluate(ST)

        elif self.value == "not":
            return not self.children[0].Evaluate(ST)

class WhileOp(Node): 
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        while self.children[0].Evaluate(ST) == True: #para passar por todos
            self.children[1].Evaluate(ST)

class IfOp(Node): 
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        if self.children[0].Evaluate(ST) == True:
            return self.children[1].Evaluate(ST)
        elif len(self.children) == 3:
            return self.children[2].Evaluate(ST)

class IntVal(Node): #0 filhos, int value
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        return self.value

class Input(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        entrada = input()
        return int(entrada)

class NoOp(Node): #0 filhos, dummy
    def __init__(self):
        pass

    def Evaluate(self, ST):
        pass

class Identifier(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        st = ST.getter(self.value)
        return st

class Assignment(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        ST.setter(self.children[0].value, self.children[1].Evaluate(ST)) #(key, value) -> a = 5 

class Statements(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        for filho in self.children:
            filho.Evaluate(ST) #vai dando evaluate em cada filho statement do nó statements

class Print(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self, ST):
        print(self.children[0].Evaluate(ST))

def main():
    try:
        #entrada  = input("Digite o que deseja calcular: ")
        arquivo = 'expressao.vbs'
        with open (arquivo, 'r') as file:
            entrada = file.read()# + "\n"
            
        codigo = PrePro.filter(entrada).rstrip() #apaga qualquer coisa que estiver no fim da string, tipo espaço
        res = Parser.run(codigo)
        ST = SymbolTable()
        res.Evaluate(ST)

    except Exception as ex:
        print(ex)

if  __name__ =='__main__':main()