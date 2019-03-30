import re
reserved = ["Print", "Begin", "End"]
Print, Begin, End = reserved

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

        elif self.origin[self.position].isalpha():
            word = ""
            while (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"): 
                word = word + self.origin[self.position]
                self.position = self.position + 1

            if word in reserved:
                self.actual = Token(word, word)
            
            else:
                self.actual = Token("identifier", word)

        else:
            raise ValueError("Caractere inválido: {}".format(self.origin[self.position]))

        return self.actual

class Parser:
    def Statements():
        if Parser.tokens.actual.type == Begin:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "\n":
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != End:
                    Parser.tokens.selectNext()
                    #######inicia um nó vazio e cada vez que passa no statement add um filho
                    left = Parser.Statement()
                    if Parser.tokens.actual.type == "\n":
                        Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == End: 
                    return left

    def Statement():
        if Parser.tokens.actual.type == "identifier":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "assignment":
                Parser.tokens.selectNext()
                left = Parser.Expression()

        elif Parser.tokens.actual.type == Print:
            Parser.tokens.selectNext()
            left = Parser.Expression()

        elif Parser.tokens.actual.type == Begin:
            ################ faz o que?

        else:
            return NoOp() ############# qual valor?


    def parseTerm():
        left = Parser.parseFactor()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div":
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("*", [left, right])
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("/", [left, right]) 
        return left

    def parseExpression():
        left = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("+", [left, right])
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                right =  Parser.parseTerm()
                left = BinOp("-", [left, right])
        return left

    def parseFactor():
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            left = IntVal(res, [])
            return left

        elif Parser.tokens.actual.type == "openpar":
            Parser.tokens.selectNext()
            res = Parser.parseExpression()
            if Parser.tokens.actual.type == "closepar":
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError('Esperava-se um fecha parênteses e foi encontrado um {}.'.format(Parser.tokens.actual.type))

        elif Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("+", [left])
                return left
            else:
                Parser.tokens.selectNext()
                left = Parser.parseFactor()
                left = UnOp("-", [left])
                return left
        
        if Parser.tokens.actual.type == "identifier":
            Parser.tokens.selectNext()
            return Identifier(valor, []) ######################################
        
        else:
            raise ValueError('Token inválido: {}'.format(Parser.tokens.actual.value))

    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.parseExpression()
        if Parser.tokens.actual.type != 'eof':
            raise ValueError('Entrada inválida. Último token não é o EOF.')
        
        return res

class PrePro:

    def filter(entrada):
        filtro = entrada.replace('\\n', '\n')
        filtro = re.sub("'.*\n", "", filtro) #para arquivos
        filtro = re.sub("'.*\r", "", filtro) #para arquivos
        filtro = re.sub("'.*", "", filtro) #apenas para o meu terminal
        return filtro   

class Node():
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos
    
    def Evaluate(self):
        pass

class BinOp(Node): #2 filhos, binary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()

        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()

        elif self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()

        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node): #1 filho, unary
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        if self.value == "+":
            return + self.children[0].Evaluate()

        elif self.value == "-":
            return - self.children[0].Evaluate()

class IntVal(Node): #0 filhos, int value
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        return self.value

class NoOp(Node): #0 filhos, dummy
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        pass

class Statements(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        ################### faz o que?
        pass

class Identifier(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        ################### faz o que?
        pass

class Assignment(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        ################### faz o que?
        pass

class Print(Node):
    def __init__(self, valor, listafilhos):
        self.value = valor
        self.children = listafilhos

    def Evaluate(self):
        ################### faz o que?
        pass

def main():
    try:
        #entrada  = input("Digite o que deseja calcular: ")
        with open ('expressao.vbs', 'r') as file:
            entrada = file.read() + "\n"
        codigo = PrePro.filter(entrada).rstrip() #apaga qualquer coisa que estiver no fim da string, tipo espaço
        res = Parser.run(codigo)
        print("Resultado:", res.Evaluate())

    except Exception as ex:
        print(ex)

if  __name__ =='__main__':main()