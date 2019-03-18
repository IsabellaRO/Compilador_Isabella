import re

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
            self.actual = Token("eof", "-1")

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

        else:
            raise ValueError("Caractere inválido.")

        return self.actual

class Parser:
    
    def parseTerm():
        res = Parser.parseFactor()
        while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div":
            if Parser.tokens.actual.type == "mult":
                Parser.tokens.selectNext()
                res = res * Parser.parseFactor()
            elif Parser.tokens.actual.type == "div":
                Parser.tokens.selectNext()
                res = res // Parser.parseFactor()    
        return res

    def parseExpression():
        res = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                res = res + Parser.parseTerm()
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                res = res - Parser.parseTerm()    
        return res

    def parseFactor():
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return res
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
                res = Parser.parseFactor()
                return res
            else:
                Parser.tokens.selectNext()
                res = Parser.parseFactor()
                return -res
        
        else:
            raise ValueError('Token inválido.')

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

def main():
    try:
        entrada  = input("Digite o que deseja calcular: ")
        codigo = PrePro.filter(entrada)
        res = Parser.run(codigo)
        print("Resultado:", res)
    except Exception as ex:
        print(ex)

if  __name__ =='__main__':main()